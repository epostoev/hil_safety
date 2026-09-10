"""
Fault Injection: отказ IMU через физическое реле (HW fault injection).

Черновик, НЕ ЗАПУСКАЛСЯ на стенде (нет доступа к HIL-стенду с этой
машины). Написан по образцу test_lidars.py/test_radars.py -- реле
192.168.1.120, relay_on(channel) снимает питание, relay_off(channel)
возвращает.

Контекст:
- rb8 -> imu_ca, rb9 -> imu_ch (подтверждено 2026-09-04, см.
  tests/fault_injection/sensing/control_relay.py:IMU_RELAY_CHANNELS).

ВАЖНО -- IMU_ERROR_CODES ЗАВЕДОМО ФЕЙКОВЫЕ (2026-09-04):
Официальных error_code для отказа IMU в /safety/mrm_request на момент
написания ЕЩЁ НЕТ (не подтверждены командой). По прямому запросу вместо
того чтобы вообще не писать тест, используются намеренно случайные
заглушки (900000001, 900000002) -- заведомо непохожие ни на один
реальный код в проекте (все существующие коды камер/лидаров/радаров --
6-значные, эти -- 9-значные, чтобы визуально не спутать).

Из-за этого тест ГАРАНТИРОВАННО падает на assert (wait_for_error_code
никогда не найдёт эти коды в /safety/mrm_request) -- это ОЖИДАЕМО и
является намеренным маркером "код не подтверждён", а не багом теста.
Как только появятся реальные error_code для imu_ca/imu_ch -- заменить
значения в IMU_ERROR_CODES ниже, и тест начнёт проверять то, что должен.

ОТКРЫТЫЕ ВОПРОСЫ:
- Реальные error_code для imu_ca/imu_ch -- см. выше, главный блокер.
- Нужен ли precondition "IMU жив" перед тестом -- в
  framework/sensing_nodes.py есть ImuNode (NODE_NAME=
  "/sensing/imu1/imu_node"), но неясно, соответствует ли она imu_ca/imu_ch
  или это третий, другой IMU. Проверка не добавлена, как и в остальных
  relay-тестах.
- Таймаут 10s взят по аналогии с test_lidars.py/test_radars.py --
  заведомо не имеет значения, пока error_code фейковые (тест всё равно
  всегда падает по таймауту).
"""
import allure
import pytest

from fault_injection.sensing.control_relay import relay_on, relay_off


# (канал реле, error_code [ЗАГЛУШКА, см. docstring], имя IMU)
IMU_CHANNELS = [
    (8, 900000001, "imu_ca"),
    (9, 900000002, "imu_ch"),
]


@allure.epic("HIL Testing")
@allure.feature("Sensing")
@allure.story("Fault Injection: HW отказ IMU через реле")
@allure.title("Fault Injection: отключение питания IMU через реле")
@allure.description(
    "Тест отключает питание конкретного IMU физическим реле (192.168.1.120, "
    "отдельный канал на IMU) и проверяет, что в /safety/mrm_request "
    "появляется соответствующий error_code ('нет данных от IMU'). "
    "ВНИМАНИЕ: error_code сейчас заглушка (реальный код не подтверждён), "
    "тест ожидаемо падает -- см. docstring файла."
)
class TestImuRelay:

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("channel, error_code, imu_name", IMU_CHANNELS)
    def test_imu_power_cut_triggers_no_data_error(
        self, channel, error_code, imu_name, mrm_monitor, request,
        restart_autopilot_after
    ):
        """
        TC-SENSING-RELAY-IMU-001..002.

        ЗАВЕДОМО ПАДАЕТ, пока error_code не заменён на реальный (см.
        docstring файла).

        После каждой проверки IMU автопилот перезапускается через
        фикстуру restart_autopilot_after (conftest.py) -- та же
        фикстура, что используется во всех kill-тестах и в
        test_lidars.py/test_radars.py.
        """
        allure.dynamic.title(
            f"Отключение {imu_name} (канал {channel}) -> "
            f"error_code {error_code} [ЗАГЛУШКА]"
        )
        allure.dynamic.parameter("channel", channel)
        allure.dynamic.parameter("imu_name", imu_name)

        request.node.expected = (
            f"В /safety/mrm_request появляется error_code "
            f"0x{error_code:08X} ({error_code}) для {imu_name} "
            f"[ЗАГЛУШКА -- реальный код не подтверждён, тест ожидаемо падает]"
        )

        with allure.step("Снять baseline: mrm_type + активные error_codes"):
            baseline = mrm_monitor.get_fields(
                ["mrm_type", "shadow_mrm_type", "drive_mode"]
            )
            baseline_codes = {e["error_code"] for e in mrm_monitor.get_error_codes()}
            allure.attach(
                f"mrm_type: {baseline['mrm_type']}\n"
                f"Активные error_codes: {sorted(baseline_codes)}",
                name="Baseline",
                attachment_type=allure.attachment_type.TEXT,
            )
            # Защита от "грязного" старта: если этот же код уже активен
            # ДО инъекции -- тест не сможет доказать причинно-следственную
            # связь. Для заглушечных кодов сработать не должна (коды
            # заведомо фейковые и не встречаются нигде реально), но
            # оставлена для единообразия с test_lidars.py/test_radars.py
            # и на случай, если код заменят на настоящий.
            if error_code in baseline_codes:
                pytest.skip(
                    f"error_code {error_code} уже активен до инъекции "
                    f"отказа -- стенд не в чистом состоянии"
                )

        with allure.step("Зафиксировать timestamp ДО отключения реле"):
            before_stamp = mrm_monitor.get_stamp()

        try:
            with allure.step(
                f"Отключить питание {imu_name} (канал {channel}, relay_on)"
            ):
                response = relay_on(channel)
                allure.attach(
                    f"status_code={response.status_code}",
                    name="Relay ON response (снимает питание)",
                    attachment_type=allure.attachment_type.TEXT,
                )

            with allure.step(
                f"Ожидать появления error_code {error_code} (timeout=10s) "
                f"[ЗАГЛУШКА -- ожидаемо НЕ появится]"
            ):
                result = mrm_monitor.wait_for_error_code(
                    error_code=error_code,
                    before_stamp=before_stamp,
                    timeout=10.0,
                    poll_interval=0.05,
                )
                allure.attach(
                    f"success:     {result['success']}\n"
                    f"reaction_ms: {result['reaction_ms']}ms\n"
                    f"details:     {result['details']}",
                    name="Результат ожидания error_code",
                    attachment_type=allure.attachment_type.TEXT,
                )

            with allure.step(
                "Assert: error_code появился "
                "[ЗАГЛУШКА -- этот assert ОЖИДАЕМО упадёт]"
            ):
                assert result["success"], (
                    f"error_code {error_code} ({imu_name}) не появился "
                    f"в /safety/mrm_request за 10s после отключения питания. "
                    f"НАПОМИНАНИЕ: этот код -- заглушка, реальный error_code "
                    f"для {imu_name} ещё не подтверждён -- см. docstring файла."
                )

            request.node.actual = (
                f"error_code {result['error_code_hex']} появился, "
                f"reaction={result['reaction_ms']}ms"
            )
            request.node.reaction_ms = f"{result['reaction_ms']}ms"

        finally:
            with allure.step(
                f"Восстановить питание {imu_name} (канал {channel}, relay_off)"
            ):
                # В finally -- чтобы стенд не остался обесточенным даже
                # при падении ассертов выше.
                relay_off(channel)