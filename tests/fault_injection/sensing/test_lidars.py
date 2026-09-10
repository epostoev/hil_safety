"""
Fault Injection: отказ лидара через физическое реле (HW fault injection).

Параметризованная версия по всем 4 лидарам НЕ ЗАПУСКАЛАСЬ на стенде --
запускалась только более ранняя одноканальная версия (канал rb15, код
131599), которая с 2026-08-07 больше не актуальна (заменена на rb4).
Черновик для ручного прогона (нет доступа к HIL-стенду с этой машины).

Контекст (подтверждено на стенде):
- Реле 192.168.1.120 управляет питанием лидаров, у каждого лидара
  ОТДЕЛЬНЫЙ канал (не общая шина):
    rb4 -> lidar_center_left -> error_code 131599
    rb5 -> lidar_left        -> error_code 262671
    rb6 -> lidar_center      -> error_code 197135
    rb7 -> lidar_right       -> error_code 328207
  (см. tests/fault_injection/sensing/control_relay.py:LIDAR_RELAY_CHANNELS)
- relay_on(channel) физически РАЗМЫКАЕТ цепь и снимает питание;
  relay_off(channel) возвращает питание -- имя функции не совпадает с
  физическим эффектом на этом блоке (подтверждено на стенде 2026-08-06/07).
- Код 263183 -- "нет данных о загрязнённости лидаров" (contamination) --
  отдельная тема, в этот файл пока не включена (неизвестно, привязан ли
  к какому-то из этих же каналов и с какой задержкой появляется).

ОТКРЫТЫЕ ВОПРОСЫ:
- Нужен ли precondition "лидар жив" перед тестом -- в
  framework/sensing_nodes.py нет отдельного класса-драйвера для лидаров
  (в отличие от RadarDriverNode/UbloxDriverNode), такой проверки здесь нет.
- Таймаут 10s взят по аналогии с kill-тестами -- для физического
  HW-отказа реакция может отличаться.
"""
import allure
import pytest

from fault_injection.sensing.control_relay import relay_on, relay_off


# (канал реле, error_code, имя лидара)
LIDAR_CHANNELS = [
    (4, 131599, "lidar_center_left"),
    (5, 262671, "lidar_left"),
    (6, 197135, "lidar_center"),
    (7, 328207, "lidar_right"),
]


@allure.epic("HIL Testing")
@allure.feature("Sensing")
@allure.story("Fault Injection: HW отказ лидара через реле")
@allure.title("Fault Injection: отключение питания лидара через реле")
@allure.description(
    "Тест отключает питание конкретного лидара физическим реле "
    "(192.168.1.120, отдельный канал на лидар) и проверяет, что в "
    "/safety/mrm_request появляется соответствующий error_code "
    "('нет данных от лидара')."
)
class TestLidarRelay:

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("channel, error_code, lidar_name", LIDAR_CHANNELS)
    def test_lidar_power_cut_triggers_no_data_error(
        self, channel, error_code, lidar_name, mrm_monitor, request,
        restart_autopilot_after
    ):
        """
        TC-SENSING-RELAY-LIDAR-001..004.

        После каждой проверки лидара автопилот перезапускается через
        фикстуру restart_autopilot_after (conftest.py) -- та же фикстура,
        что используется во всех kill-тестах. Она ничего не делает до
        yield и не используется по имени в теле теста -- вся её работа
        (kill "drive", ожидание 120с, повторный запуск, ожидание
        mrm_type: 2 -> 0) происходит в teardown, после завершения теста.
        """
        allure.dynamic.title(
            f"Отключение {lidar_name} (канал {channel}) -> "
            f"error_code {error_code}"
        )
        allure.dynamic.parameter("channel", channel)
        allure.dynamic.parameter("lidar_name", lidar_name)

        request.node.expected = (
            f"В /safety/mrm_request появляется error_code "
            f"0x{error_code:08X} ({error_code}) для {lidar_name}"
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
                f"Отключить питание {lidar_name} (канал {channel}, relay_on)"
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
                    f"error_code {error_code} ({lidar_name}) не появился "
                    f"в /safety/mrm_request за 10s после отключения питания"
                )

            request.node.actual = (
                f"error_code {result['error_code_hex']} появился, "
                f"reaction={result['reaction_ms']}ms"
            )
            request.node.reaction_ms = f"{result['reaction_ms']}ms"

        finally:
            with allure.step(
                f"Восстановить питание {lidar_name} (канал {channel}, relay_off)"
            ):
                # В finally -- чтобы стенд не остался обесточенным даже
                # при падении ассертов выше.
                relay_off(channel)