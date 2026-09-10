"""
Fault Injection: отказ камеры через порчу конфига на TZTEK
(HW/config-level fault injection).

Черновик, НЕ ЗАПУСКАЛСЯ на стенде (нет доступа к HIL-стенду с этой
машины). Написан по образцу test_lidars.py/test_radars.py, но вместо
физического реле (control_relay.py) используется TZTEK
(tests/fault_injection/sensing/tztek_control.py) -- устройство,
обрабатывающее видеопоток с каждой камеры.

Механизм fault injection (проверено вручную инженером стенда 2026-08-28):
1. GET  /config?camera=<name>  -- прочитать ТЕКУЩИЙ конфиг камеры.
   Этот же JSON служит бэкапом для восстановления после теста.
2. POST /config?camera=<name>  с тем же JSON, но с "port" изменённым на
   заведомо неправильный (BROKEN_PORT=7000 вместо реального) -- камера
   перестаёт присылать поток по ожидаемому адресу, что в итоге долетает
   как ошибка в /safety/mrm_request.
3. После теста -- POST оригинального конфига обратно (восстановление).

reboot_tztek() НЕ используется вообще (закомментирован, оставлен в
tztek_control.py на будущее). Первый прогон без reboot (2026-08-31/09-04)
показал, что список error_codes в /safety/mrm_request не очищается
синхронно с mrm_type -- коды уже "починенных" камер продолжают висеть
активными дольше, чем mrm_type. Из-за этого проверка "код уже активен в
baseline -- считаем грязным стартом и скипаем" стала бесполезной: она
скипала честные тесты (leopard120_2, leopard120_3), у которых код
появился в baseline не из-за них самих, а как побочный эффект от порчи
предыдущей камеры.

РЕШЕНИЕ (с 2026-09-04, по прямому запросу): проверка "грязного старта"
УБРАНА ПОЛНОСТЬЮ. Критерий успеха теста теперь простой и единственный --
error_code данной конкретной камеры появился в СООБЩЕНИИ /safety/mrm_request,
пришедшем ПОСЛЕ before_stamp (момента непосредственно перед порчей
конфига именно этой камеры). Это уже гарантируется механизмом
wait_for_error_code(before_stamp=...) -- отдельная ручная проверка
baseline_codes была избыточна и, как показал прогон, вредна (давала
ложные skip).

ВАЖНАЯ ОГОВОРКА (осознанный компромисс, принят вместе с решением выше):
если error_code данной камеры к моменту теста уже висел активным по
ПОСТОРОННЕЙ причине (например, как раз из-за незачищенного состояния от
предыдущей камеры) и MRM продолжает периодически переотправлять текущий
список активных ошибок в каждом новом сообщении -- wait_for_error_code
формально увидит "новое сообщение с нужным кодом" и засчитает PASS, даже
если porча конфига в этом конкретном прогоне ничего не сделала. Строгая
причинно-следственная связь (как в лидарах/радарах, где такой проблемы
не было) здесь не гарантирована -- ровно об этом предупреждали при show
baseline_codes раньше. Принято как известный компромисс ради простоты и
отсутствия reboot.

Все 8 камер прогоняются в РАМКАХ ОДНОГО запуска drive -- restart_autopilot_after
НЕ используется (в отличие от test_lidars.py/test_radars.py и kill-тестов).
Это оправдано тем, что здесь ломается не сам процесс/нода (никакого
kill -N), а внешнее устройство (TZTEK) -- как только конфиг восстановлен и
TZTEK перезагружен, поток должен возобновиться сам, без необходимости
перезапускать drive. Вместо перезапуска drive в конце каждого теста явно
ждём возврата mrm_type к значению ДО инъекции (wait_for_mrm_type_change) --
это нужно, чтобы следующая камера в этом же прогоне не унаследовала ещё не
рассосавшееся состояние fault от предыдущей.

Соответствие камера -> error_code подтверждено на стенде 2026-08-28/31:
    leopard120_1 -> 65807
    leopard120_2 -> 131343
    leopard120_3 -> 196879
    leopard120_4 -> 262415
    leopard120_5 -> 327951
    leopard120_6 -> 393487
    leopard120_7 -> 459023
    leopard120_8 -> 524559

ОТКРЫТЫЕ ВОПРОСЫ:
- Нужен ли precondition "камера жива" перед тестом -- в
  framework/sensing_nodes.py есть CameraDecoderNode
  (NODE_NAME="/sensing/camera_decoder"), но это ОДНА нода на весь
  декодер, не по классу на каждую физическую камеру. Проверка не
  добавлена, как и в test_lidars.py/test_radars.py.
- Таймаут 10s взят по аналогии с test_lidars.py/test_radars.py -- для
  порчи конфига (в отличие от физического обесточивания) реакция может
  отличаться, не проверено.
- Что если set_camera_config() в шаге восстановления (finally) не
  отработает (TZTEK недоступен, таймаут и т.п.) -- камера останется
  сломанной до ручного вмешательства. В relay-тестах та же самая
  структура рисков (relay_off() тоже может не отработать), это
  системное свойство паттерна try/finally с внешним HTTP-вызовом, а не
  что-то специфичное для камер.
"""
import allure
import pytest

from fault_injection.sensing.tztek_control import (
    BROKEN_PORT,
    get_camera_config,
    set_camera_config,
)
# reboot_tztek, REBOOT_WAIT_SECONDS -- временно не используются, см.
# docstring файла. import time тоже не нужен без time.sleep(REBOOT_WAIT_SECONDS).


# (имя камеры, error_code)
CAMERA_ERROR_CODES = [
    ("leopard120_1", 65807),
    ("leopard120_2", 131343),
    ("leopard120_3", 196879),
    ("leopard120_4", 262415),
    ("leopard120_5", 327951),
    ("leopard120_6", 393487),
    ("leopard120_7", 459023),
    ("leopard120_8", 524559),
]


@allure.epic("HIL Testing")
@allure.feature("Sensing")
@allure.story("Fault Injection: отказ камеры через порчу конфига (TZTEK)")
@allure.title("Fault Injection: порча конфига камеры через TZTEK")
@allure.description(
    "Тест меняет порт конкретной камеры на заведомо неправильный через "
    "TZTEK (192.168.1.101:8080) и проверяет, что в /safety/mrm_request "
    "появляется соответствующий error_code ('нет данных от камеры')."
)
class TestCameraConfigFault:

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("camera_name, error_code", CAMERA_ERROR_CODES)
    def test_camera_config_break_triggers_no_data_error(
        self, camera_name, error_code, mrm_monitor, request
    ):
        """
        TC-SENSING-TZTEK-CAM-001..008.

        В ОТЛИЧИЕ от kill-тестов и test_lidars.py/test_radars.py -- НЕ
        перезапускает drive (нет restart_autopilot_after). Все 8 камер
        прогоняются подряд в рамках одного запуска drive. Вместо этого в
        конце теста явно ждём возврата mrm_type к baseline-значению
        (см. finally) -- чтобы следующая камера стартовала на чистом
        состоянии.
        """
        allure.dynamic.title(
            f"Порча конфига {camera_name} (port -> {BROKEN_PORT}) -> "
            f"error_code {error_code}"
        )
        allure.dynamic.parameter("camera_name", camera_name)

        request.node.expected = (
            f"В /safety/mrm_request появляется error_code "
            f"0x{error_code:08X} ({error_code}) для {camera_name}"
        )

        with allure.step("Снять baseline: mrm_type + активные error_codes"):
            # Проверка "грязного старта" здесь намеренно НЕ делается -- см.
            # docstring файла (2026-09-04). baseline_codes всё ещё
            # собирается и прикладывается к отчёту -- полезно для
            # диагностики руками, даже если тест по нему больше не skip'ается.
            baseline = mrm_monitor.get_fields(
                ["mrm_type", "shadow_mrm_type", "drive_mode"]
            )
            baseline_codes = {e["error_code"] for e in mrm_monitor.get_error_codes()}
            allure.attach(
                f"mrm_type: {baseline['mrm_type']}\n"
                f"Активные error_codes: {sorted(baseline_codes)}\n"
                f"error_code этой камеры уже в baseline: "
                f"{error_code in baseline_codes}",
                name="Baseline",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step(f"Прочитать текущий конфиг {camera_name} (backup)"):
            original_config = get_camera_config(camera_name)
            allure.attach(
                str(original_config),
                name=f"Оригинальный конфиг {camera_name}",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Зафиксировать timestamp ДО порчи конфига"):
            before_stamp = mrm_monitor.get_stamp()

        try:
            with allure.step(
                f"Испортить конфиг {camera_name} (port -> {BROKEN_PORT})"
            ):
                broken_config = dict(original_config)
                broken_config["port"] = BROKEN_PORT
                response = set_camera_config(camera_name, broken_config)
                allure.attach(
                    f"status_code={response.status_code}",
                    name="Set broken config response",
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
                    f"error_code {error_code} ({camera_name}) не появился "
                    f"в /safety/mrm_request за 10s после порчи конфига"
                )

            request.node.actual = (
                f"error_code {result['error_code_hex']} появился, "
                f"reaction={result['reaction_ms']}ms"
            )
            request.node.reaction_ms = f"{result['reaction_ms']}ms"

        finally:
            with allure.step(f"Восстановить оригинальный конфиг {camera_name}"):
                # В finally -- чтобы камера не осталась сломанной даже
                # при падении ассертов выше.
                response = set_camera_config(camera_name, original_config)
                allure.attach(
                    f"status_code={response.status_code}",
                    name="Restore config response",
                    attachment_type=allure.attachment_type.TEXT,
                )

            # ВРЕМЕННО ОТКЛЮЧЕНО (2026-09-04, по просьбе) -- см. docstring
            # файла. Раскомментировать вместе с импортом reboot_tztek,
            # REBOOT_WAIT_SECONDS и `import time`, если "грязный старт"
            # вернётся у следующих по порядку камер без reboot.
            #
            # with allure.step(
            #     f"Перезагрузить TZTEK и подождать {REBOOT_WAIT_SECONDS}с"
            # ):
            #     # Восстановления конфига одного недостаточно -- TZTEK не
            #     # поднимает поток обратно без полной перезагрузки
            #     # устройства. Выполняется ПОСЛЕ восстановления конфига --
            #     # если бы порядок был обратным, устройство могло бы
            #     # подняться со сломанным конфигом, если он успел
            #     # сохраниться на диск.
            #     reboot_result = reboot_tztek()
            #     allure.attach(
            #         f"returncode: {reboot_result.returncode}\n"
            #         f"stdout: {reboot_result.stdout}\n"
            #         f"stderr: {reboot_result.stderr}",
            #         name="reboot_tztek() result",
            #         attachment_type=allure.attachment_type.TEXT,
            #     )
            #     time.sleep(REBOOT_WAIT_SECONDS)

            with allure.step(
                "Дождаться возврата mrm_type к исходному значению "
                "(drive НЕ перезапускается -- следующая камера в этом же "
                "прогоне должна стартовать на чистом состоянии)"
            ):
                recovery = mrm_monitor.wait_for_mrm_type_change(
                    from_value="2",
                    to_value=baseline["mrm_type"] or "0",
                    timeout=60.0,
                    poll_interval=0.5,
                )
                allure.attach(
                    str(recovery),
                    name="Результат ожидания восстановления mrm_type",
                    attachment_type=allure.attachment_type.TEXT,
                )
                if not recovery["success"]:
                    # Не роняем тест здесь -- основной assert (error_code
                    # появился) уже отработал выше. Но громко предупреждаем:
                    # если mrm_type не вернулся, baseline_codes-проверка
                    # следующей камеры в этом же прогоне ещё может поймать
                    # "грязный старт" через error_code, но НЕ поймает
                    # ситуацию "mrm_type всё ещё 2 по другой причине" --
                    # эту ситуацию нужно смотреть в логе вручную.
                    print(
                        f"[WARNING] mrm_type не вернулся к "
                        f"{baseline['mrm_type']} за 60с после восстановления "
                        f"{camera_name}. Следующий тест может начаться "
                        f"на незавершившемся recovery -- проверьте вручную."
                    )