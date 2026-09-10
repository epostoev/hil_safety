"""
Общая реализация fault injection сценария "kill -6 ноды -> проверка MRM".

До рефакторинга (2026-08-04) этот сценарий был построчно продублирован
в 9 файлах tests/fault_injection/test_*_kill.py (см.
tests/fault_injection/KNOWN_ISSUES.md, пункт 10). Каждый файл теперь
вызывает run_kill_fault_injection() как тонкую обёртку, оставляя себе
только allure-метаданные (epic/feature/story) и список нод.
"""
import json
import time

import allure
import pytest


NODE_DOWN_ERROR_CODE = 131346


def run_kill_fault_injection(
    node,
    node_name: str,
    mrm_monitor,
    request,
    sla_ms: float = 5000,
    error_code: int = NODE_DOWN_ERROR_CODE,
) -> None:
    """
    Отправляет kill -6 ноде и проверяет реакцию MRM (/safety/mrm_request).

    Критерий прохождения: node_name появляется в details.nodes записи
    error_codes с кодом error_code (по умолчанию 131346 -- watchdog
    "нода недоступна"). mrm_type сейчас не проверяется -- см.
    tests/fault_injection/KNOWN_ISSUES.md, пункт 15.

    :param node: объект ноды (BaseHILTest), уже полученный из фикстуры.
    :param node_name: строковое ROS-имя ноды (должно совпадать с записью
        в details.nodes error_code, например "/calibration/rct/rct_validator").
    :param mrm_monitor: session-scoped MrmRequestMonitor.
    :param request: pytest request (для request.node.expected/actual/reaction_ms).
    :param sla_ms: заявленный SLA по времени появления error_code в миллисекундах.
    :param error_code: код ошибки, в details.nodes которого должна появиться node_name.
    """
    request.node.expected = (
        f"{node_name} появляется в details.nodes error_code {error_code} "
        f"в /safety/mrm_request. Время реакции < {sla_ms:g}ms"
    )

    if not node.is_alive():
        pytest.skip(f"Нода {node_name} не запущена")

    with allure.step("Снять baseline: mrm_type, shadow_mrm_type, drive_mode"):
        baseline = mrm_monitor.get_fields(["mrm_type", "shadow_mrm_type", "drive_mode"])
        node.logger.info(f"Baseline mrm_type={baseline['mrm_type']}")
        allure.attach(
            f"mrm_type:        {baseline['mrm_type']}\n"
            f"shadow_mrm_type: {baseline['shadow_mrm_type']}\n"
            f"drive_mode:      {baseline['drive_mode']}",
            name="Baseline",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(
        f"Защита от грязного старта: {node_name} не должна быть "
        f"в details.nodes error_code {error_code} ДО kill"
    ):
        baseline_nodes = mrm_monitor._nodes_in_error_code(error_code)
        allure.attach(
            "\n".join(baseline_nodes) or "нет",
            name=f"Baseline nodes в error_code {error_code}",
            attachment_type=allure.attachment_type.TEXT,
        )
        if node_name in baseline_nodes:
            pytest.skip(
                f"{node_name} уже в details.nodes error_code {error_code} "
                f"ДО kill -- стенд не в чистом состоянии, "
                f"тест не докажет причинно-следственную связь"
            )

    with allure.step(f"Получить PID ноды {node_name}"):
        pid_before = node.get_pid()
        node.logger.info(f"PID={pid_before}")
        allure.attach(
            str(pid_before),
            name="PID до kill",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Зафиксировать timestamp перед kill"):
        before_stamp = mrm_monitor.get_stamp()
        node.logger.info(f"Stamp ДО kill: {before_stamp}")

    with allure.step(f"Отправить kill -6 PID={pid_before}"):
        node.run_docker_command(f"kill -6 {pid_before}")
        node.logger.info(
            f"kill -6 отправлен PID={pid_before}. "
            f"Ждём появления {node_name} в error_code {error_code}..."
        )

    with allure.step(
        f"Ожидать {node_name} в details.nodes error_code {error_code} "
        f"(timeout=10s)"
    ):
        result = mrm_monitor.wait_for_node_in_error_code(
            error_code=error_code,
            node_name=node_name,
            before_stamp=before_stamp,
            timeout=10.0,
            poll_interval=0.01
        )
        node.logger.info(
            f"Результат: success={result['success']}, "
            f"reaction={result['reaction_ms']}ms "
            f"({result['reaction_ns']}ns), "
            f"nodes={result['nodes']}"
        )
        allure.attach(
            f"success:      {result['success']}\n"
            f"error_code:   {result['error_code_hex']} ({result['error_code']})\n"
            f"nodes:        {result['nodes']}\n"
            f"reaction_ms:  {result['reaction_ms']}ms\n"
            f"reaction_ns:  {result['reaction_ns']}ns",
            name="Результат ожидания error_code",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Собрать error_codes после kill"):
        error_codes = mrm_monitor.get_error_codes()
        triggered_errors = [
            e for e in error_codes
            if e["details"] != "{}"
        ]
        node.logger.info(f"Triggered errors: {len(triggered_errors)}")
        for e in triggered_errors:
            node.logger.info(
                f"  {e['error_code_hex']} ({e['error_code']}): "
                f"{e['details'][:80]}"
            )
        errors_text = "\n".join([
            f"{e['error_code_hex']} ({e['error_code']}): {e['details'][:80]}"
            for e in triggered_errors
        ]) or "нет"
        allure.attach(
            errors_text,
            name=f"Triggered errors ({len(triggered_errors)})",
            attachment_type=allure.attachment_type.TEXT,
        )
        # Сохраняем error_codes в файл и прикрепляем к отчёту
        log_path = f"/tmp/error_codes_{node_name.replace('/', '_')}.json"
        with open(log_path, "w") as f:
            json.dump(triggered_errors, f, indent=2, ensure_ascii=False)
        allure.attach.file(
            log_path,
            name=f"error_codes_{node_name}",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Проверить наличие авторестарта ноды (fault tolerance)"):
        time.sleep(3)
        if node.is_alive():
            node.has_auto_restart = True
            node.logger.info(
                "drive.py перезапустил ноду. "
                "Fault tolerance: ПОДТВЕРЖДЁН ✅"
            )
            allure.attach(
                f"Нода {node_name} перезапущена автоматически\n"
                "Fault Tolerance: ПОДТВЕРЖДЁН ✅",
                name="Fault Tolerance",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            allure.attach(
                f"Авторестарт {node_name} не обнаружен за 3 секунды",
                name="Fault Tolerance",
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step(
        f"Проверить assert: {node_name} появилась в details.nodes "
        f"error_code {error_code}"
    ):
        assert result["success"], (
            f"{node_name} не появилась в details.nodes error_code "
            f"{error_code} за 10s после kill -6. "
            f"Текущий список нод: {result['nodes']}"
        )

    with allure.step(f"Проверить SLA: время реакции < {sla_ms:g}ms"):
        assert result["reaction_ms"] < sla_ms, (
            f"Время реакции {result['reaction_ms']}ms превышает "
            f"заявленный SLA {sla_ms:g}ms"
        )

    errors_str = " | ".join([
        f"{e['error_code_hex']}: {e['details'][:50]}"
        for e in triggered_errors
    ]) or "нет"

    request.node.actual = (
        f"{node_name} появилась в error_code {result['error_code_hex']} "
        f"({result['error_code']}), reaction={result['reaction_ms']}ms. "
        f"Ошибки: {errors_str} ✅"
    )
    request.node.reaction_ms = f"{result['reaction_ms']}ms"

    if node.has_auto_restart:
        node.logger.info(
            f"Fault tolerance: ПОДТВЕРЖДЁН ✅ "
            f"Время реакции MRM: {result['reaction_ms']}ms"
        )

# """
# Общая реализация fault injection сценария "kill -6 ноды -> проверка MRM".

# До рефакторинга (2026-08-04) этот сценарий был построчно продублирован
# в 9 файлах tests/fault_injection/test_*_kill.py (см.
# tests/fault_injection/KNOWN_ISSUES.md, пункт 10). Каждый файл теперь
# вызывает run_kill_fault_injection() как тонкую обёртку, оставляя себе
# только allure-метаданные (epic/feature/story) и список нод.
# """
# import json
# import time

# import allure
# import pytest


# def run_kill_fault_injection(
#     node,
#     node_name: str,
#     mrm_monitor,
#     request,
#     sla_ms: float = 5000,
# ) -> None:
#     """
#     Отправляет kill -6 ноде и проверяет реакцию MRM (/safety/mrm_request).

#     :param node: объект ноды (BaseHILTest), уже полученный из фикстуры.
#     :param node_name: строковое ROS-имя ноды, только для логов/отчёта.
#     :param mrm_monitor: session-scoped MrmRequestMonitor.
#     :param request: pytest request (для request.node.expected/actual/reaction_ms).
#     :param sla_ms: заявленный SLA по времени реакции MRM в миллисекундах.
#     """
#     request.node.expected = f"mrm_type: 0 → 2. Время реакции < {sla_ms:g}ms"

#     if not node.is_alive():
#         pytest.skip(f"Нода {node_name} не запущена")

#     with allure.step("Снять baseline: mrm_type, shadow_mrm_type, drive_mode"):
#         baseline = mrm_monitor.get_fields(["mrm_type", "shadow_mrm_type", "drive_mode"])
#         node.logger.info(f"Baseline mrm_type={baseline['mrm_type']}")
#         allure.attach(
#             f"mrm_type:        {baseline['mrm_type']}\n"
#             f"shadow_mrm_type: {baseline['shadow_mrm_type']}\n"
#             f"drive_mode:      {baseline['drive_mode']}",
#             name="Baseline",
#             attachment_type=allure.attachment_type.TEXT,
#         )

#     with allure.step(f"Получить PID ноды {node_name}"):
#         pid_before = node.get_pid()
#         node.logger.info(f"PID={pid_before}")
#         allure.attach(
#             str(pid_before),
#             name="PID до kill",
#             attachment_type=allure.attachment_type.TEXT,
#         )

#     with allure.step("Зафиксировать timestamp перед kill"):
#         before_stamp = mrm_monitor.get_stamp()
#         node.logger.info(f"Stamp ДО kill: {before_stamp}")

#     with allure.step(f"Отправить kill -6 PID={pid_before}"):
#         node.run_docker_command(f"kill -6 {pid_before}")
#         node.logger.info(
#             f"kill -6 отправлен PID={pid_before}. "
#             f"Ждём изменения mrm_type..."
#         )

#     with allure.step("Ожидать mrm_type: 0 → 2 (timeout=10s)"):
#         result = mrm_monitor.wait_for_mrm_type_change(
#             from_value="0",
#             to_value="2",
#             before_stamp=before_stamp,
#             timeout=10.0,
#             poll_interval=0.01
#         )
#         node.logger.info(
#             f"Результат: success={result['success']}, "
#             f"reaction={result['reaction_ms']}ms "
#             f"({result['reaction_ns']}ns), "
#             f"mrm_type={result['mrm_type']}"
#         )
#         allure.attach(
#             f"success:      {result['success']}\n"
#             f"mrm_type:     {result['mrm_type']}\n"
#             f"reaction_ms:  {result['reaction_ms']}ms\n"
#             f"reaction_ns:  {result['reaction_ns']}ns",
#             name="Результат ожидания MRM",
#             attachment_type=allure.attachment_type.TEXT,
#         )

#     with allure.step("Собрать error_codes после kill"):
#         error_codes = mrm_monitor.get_error_codes()
#         triggered_errors = [
#             e for e in error_codes
#             if e["details"] != "{}"
#         ]
#         node.logger.info(f"Triggered errors: {len(triggered_errors)}")
#         for e in triggered_errors:
#             node.logger.info(
#                 f"  {e['error_code_hex']} ({e['error_code']}): "
#                 f"{e['details'][:80]}"
#             )
#         errors_text = "\n".join([
#             f"{e['error_code_hex']} ({e['error_code']}): {e['details'][:80]}"
#             for e in triggered_errors
#         ]) or "нет"
#         allure.attach(
#             errors_text,
#             name=f"Triggered errors ({len(triggered_errors)})",
#             attachment_type=allure.attachment_type.TEXT,
#         )
#         # Сохраняем error_codes в файл и прикрепляем к отчёту
#         log_path = f"/tmp/error_codes_{node_name.replace('/', '_')}.json"
#         with open(log_path, "w") as f:
#             json.dump(triggered_errors, f, indent=2, ensure_ascii=False)
#         allure.attach.file(
#             log_path,
#             name=f"error_codes_{node_name}",
#             attachment_type=allure.attachment_type.JSON,
#         )

#     with allure.step("Проверить наличие авторестарта ноды (fault tolerance)"):
#         time.sleep(3)
#         if node.is_alive():
#             node.has_auto_restart = True
#             node.logger.info(
#                 "drive.py перезапустил ноду. "
#                 "Fault tolerance: ПОДТВЕРЖДЁН ✅"
#             )
#             allure.attach(
#                 f"Нода {node_name} перезапущена автоматически\n"
#                 "Fault Tolerance: ПОДТВЕРЖДЁН ✅",
#                 name="Fault Tolerance",
#                 attachment_type=allure.attachment_type.TEXT,
#             )
#         else:
#             allure.attach(
#                 f"Авторестарт {node_name} не обнаружен за 3 секунды",
#                 name="Fault Tolerance",
#                 attachment_type=allure.attachment_type.TEXT,
#             )

#     with allure.step("Проверить assert: mrm_type изменился на '2'"):
#         assert result["success"], (
#             f"mrm_type не изменился на '2'. "
#             f"Текущее значение: {result['mrm_type']}"
#         )

#     with allure.step(f"Проверить SLA: время реакции < {sla_ms:g}ms"):
#         assert result["reaction_ms"] < sla_ms, (
#             f"Время реакции {result['reaction_ms']}ms превышает "
#             f"заявленный SLA {sla_ms:g}ms"
#         )

#     errors_str = " | ".join([
#         f"{e['error_code_hex']}: {e['details'][:50]}"
#         for e in triggered_errors
#     ]) or "нет"

#     request.node.actual = (
#         f"mrm_type: {baseline['mrm_type']} → {result['mrm_type']}. "
#         f"Ошибки: {errors_str} ✅"
#     )
#     request.node.reaction_ms = f"{result['reaction_ms']}ms"

#     if node.has_auto_restart:
#         node.logger.info(
#             f"Fault tolerance: ПОДТВЕРЖДЁН ✅ "
#             f"Время реакции MRM: {result['reaction_ms']}ms"
#         )