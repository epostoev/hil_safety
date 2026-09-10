import pytest
import allure

from framework.kill_fault_injection import run_kill_fault_injection


PLANNING_NODES = [
    ("planning_maneuver_planner_node",              "TC-PLA-PRE-001", "/planning/maneuver_planner_node"),
    ("planning_lane_tracer_node",                   "TC-PLA-PRE-002", "/planning/lane_tracer_node"),
    ("planning_trajectory_planner_node",            "TC-PLA-PRE-003", "/planning/trajectory_planner_node"),
    ("planning_path_loader_node",                   "TC-PLA-PRE-004", "/planning/path_loader_node"),
    # ("planning_approximate_paths_publisher_node",   "TC-PLA-PRE-005", "/planning/approximate_paths_publisher_node"),
    # ("planning_trajectory_validator_node",          "TC-PLA-PRE-006", "/planning/trajectory_validator_node"),
    ("planning_visualization_node",                 "TC-PLA-PRE-007", "/planning/visualization/planning_visualization_node"),
    # ("planning_ml_planner_cpp_node",                "TC-PLA-PRE-008", "/planning/ml_planner_cpp"),
]

@allure.epic("HIL Testing")
@allure.feature("Planning")
@allure.story("Fault Injection: kill -6 нод")
@allure.title("Fault Injection: принудительное завершение нод компонента Planning")
@allure.description(
    "Тест отправляет kill -6 каждой ноде компонента Planning "
    "и проверяет что MRM реагирует переходом mrm_type: 0 → 2 "
    "в течение 5000ms."
)
class TestPlanningKill:

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", PLANNING_NODES)
    def test_planning_kill(self, fixture_name, tc_id, node_name,
                           mrm_monitor, request, restart_autopilot_after):

        allure.dynamic.title(f"{tc_id}: kill -6 {node_name}")
        allure.dynamic.parameter("node_name", node_name)
        allure.dynamic.parameter("tc_id", tc_id)

        with allure.step(f"Получить объект ноды {node_name}"):
            node = request.getfixturevalue(fixture_name)

        run_kill_fault_injection(node, node_name, mrm_monitor, request, sla_ms=5000)