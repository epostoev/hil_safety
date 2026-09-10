import pytest
import allure

from framework.kill_fault_injection import run_kill_fault_injection


HDMAP_NODES = [
    ("hdmap_service_node_alive",            "TC-HDM-KILL-001", "/hdmap_service_node"),
    ("hdmap_dynamic_objects_service_alive", "TC-HDM-KILL-002", "/dynamic_objects_service_node"),
    ("hdmap_rtk_provider_node_alive",       "TC-HDM-KILL-003", "/rtk_provider_node"),
    # ("hdmap_issue_reporter_node_alive",     "TC-HDM-KILL-004", "/hdmap/issue_reporter"),
    # ("hdmap_visualization_node_alive",      "TC-HDM-KILL-005", "/hdmap/visualization/hdmap_visualization_node"),
]


@allure.epic("HIL Testing")
@allure.feature("HD-Map")
@allure.story("Fault Injection: kill -6 нод")
@allure.title("Fault Injection: принудительное завершение нод компонента HD-Map")
@allure.description(
    "Тест отправляет kill -6 каждой ноде компонента HD-Map "
    "и проверяет что MRM реагирует переходом mrm_type: 0 → 2 "
    "в течение 5000ms."
)
class TestHdmapKill:
    """
    Fault Injection: принудительное завершение нод компонента HD-Map.

    TC-HDM-KILL-001: /hdmap_service_node
    TC-HDM-KILL-002: /dynamic_objects_service_node
    TC-HDM-KILL-003: /rtk_provider_node
    TC-HDM-KILL-004: /hdmap/issue_reporter
    TC-HDM-KILL-005: /hdmap/visualization/hdmap_visualization_node
    """

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", HDMAP_NODES)
    def test_hdmap_kill(self, fixture_name, tc_id, node_name,
                        mrm_monitor, request, restart_autopilot_after):

        allure.dynamic.title(f"{tc_id}: kill -6 {node_name}")
        allure.dynamic.parameter("node_name", node_name)
        allure.dynamic.parameter("tc_id", tc_id)

        with allure.step(f"Получить объект ноды {node_name}"):
            node = request.getfixturevalue(fixture_name)

        run_kill_fault_injection(node, node_name, mrm_monitor, request, sla_ms=5000)