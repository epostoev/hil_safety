"""
Fault Injection: отказ радара через физическое реле (HW fault injection).

Черновик, НЕ ЗАПУСКАЛСЯ на стенде (нет доступа к HIL-стенду с этой
машины). Написан по образцу test_lidars.py -- та же схема (relay_on
снимает питание, relay_off возвращает, wait_for_error_code ждёт появления
конкретного error_code в /safety/mrm_request), только другие каналы
реле и коды ошибок.

Контекст (подтверждено на стенде 2026-08-24):
- Реле 192.168.1.120 управляет питанием радаров, у каждого радара
  ОТДЕЛЬНЫЙ канал (не общая шина):
    rb0 -> radar_roof_back_left   -> error_code 459535
    rb1 -> radar_roof_back_right  -> error_code 393999
    rb2 -> radar_roof_front_right -> error_code 66319
    rb3 -> radar_roof_front_left  -> error_code 131855
  (см. tests/fault_injection/sensing/control_relay.py:RADAR_RELAY_CHANNELS)
- relay_on(channel) физически РАЗМЫКАЕТ цепь и снимает питание;
  relay_off(channel) возвращает питание -- имя функции не совпадает с
  физическим эффектом (та же оговорка, что и для лидаров, см.
  control_relay.py).

ОТКРЫТЫЕ ВОПРОСЫ:
- Нужен ли precondition "радар жив" перед тестом -- в
  framework/sensing_nodes.py есть RadarDriverNode
  (NODE_NAME="/sensing/radar_driver_node"), но это ОДНА нода на весь
  радарный стек, не по одному классу на каждый физический радар (в
  отличие от лидаров, где такого класса нет вообще). Неясно, повлияет ли
  отключение одного радара на is_alive() этой общей ноды -- проверка не
  добавлена, как и в test_lidars.py.
- Таймаут 10s взят по аналогии с test_lidars.py -- для радаров реакция
  может отличаться от лидаров, не проверено.
"""
import allure
import pytest

from fault_injection.sensing.control_relay import relay_on, relay_off


# (канал реле, error_code, имя радара)
RADAR_CHANNELS = [
    (0, 459535, "radar_roof_back_left"),
    (1, 393999, "radar_roof_back_right"),
    (2, 66319, "radar_roof_front_right"),
    (3, 131855, "radar_roof_front_left"),
]


@allure.epic("HIL Testing")
@allure.feature("Sensing")
@allure.story("Fault Injection: HW отказ радара через реле")
@allure.title("Fault Injection: отключение питания радара через реле")
@allure.description(
    "Тест отключает питание конкретного радара физическим реле "
    "(192.168.1.120, отдельный канал на радар) и проверяет, что в "
    "/safety/mrm_request появляется соответствующий error_code "
    "('нет данных от радара')."
)
class TestRadarRelay:

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("channel, error_code, radar_name", RADAR_CHANNELS)
    def test_radar_power_cut_triggers_no_data_error(
        self, channel, error_code, radar_name, mrm_monitor, request,
        restart_autopilot_after
    ):
        """
        TC-SENSING-RELAY-RADAR-001..004.

        После каждой проверки радара автопилот перезапускается через
        фикстуру restart_autopilot_after (conftest.py) -- та же фикстура,
        что используется во всех kill-тестах и в test_lidars.py. Вся её
        работа (kill "drive", ожидание 120с, повторный запуск, ожидание
        mrm_type: 2 -> 0) происходит в teardown, после завершения теста.
        """
        allure.dynamic.title(
            f"Отключение {radar_name} (канал {channel}) -> "
            f"error_code {error_code}"
        )
        allure.dynamic.parameter("channel", channel)
        allure.dynamic.parameter("radar_name", radar_name)

        request.node.expected = (
            f"В /safety/mrm_request появляется error_code "
            f"0x{error_code:08X} ({error_code}) для {radar_name}"
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
            # связь (см. случай с cloud_builder_node 2026-08-05).
            if error_code in baseline_codes:
                pytest.skip(
                    f"error_code {error_code} уже активен до инъекции "
                    f"отказа -- стенд не в чистом состоянии"
                )

        with allure.step("Зафиксировать timestamp ДО отключения реле"):
            before_stamp = mrm_monitor.get_stamp()

        try:
            with allure.step(
                f"Отключить питание {radar_name} (канал {channel}, relay_on)"
            ):
                response = relay_on(channel)
                allure.attach(
                    f"status_code={response.status_code}",
                    name="Relay ON response (снимает питание)",
                    attachment_type=allure.attachment_type.TEXT,
                )

            with allure.step(
                f"Ожидать появления error_code {error_code} (timeout=10s)"
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

            with allure.step("Assert: error_code появился"):
                assert result["success"], (
                    f"error_code {error_code} ({radar_name}) не появился "
                    f"в /safety/mrm_request за 10s после отключения питания"
                )

            request.node.actual = (
                f"error_code {result['error_code_hex']} появился, "
                f"reaction={result['reaction_ms']}ms"
            )
            request.node.reaction_ms = f"{result['reaction_ms']}ms"

        finally:
            with allure.step(
                f"Восстановить питание {radar_name} (канал {channel}, relay_off)"
            ):
                # В finally -- чтобы стенд не остался обесточенным даже
                # при падении ассертов выше.
                relay_off(channel)