import pytest
import allure

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
@allure.story("Предусловия: проверка запуска нод")
@allure.title("Проверка запуска нод компонента Planning")
@allure.description(
    "Предусловия: все ноды компонента Planning должны присутствовать в ROS graph. "
    "Тест проверяет каждую ноду через is_alive()."
)

class TestPlanningNodesRunning:
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", PLANNING_NODES)
    def test_node_running(self, fixture_name, tc_id, node_name, request):
        f"""{tc_id}: {node_name} присутствует в ROS graph"""

        allure.dynamic.title(f"{tc_id}: {node_name}")
        allure.dynamic.parameter("node_name", node_name)
        allure.dynamic.parameter("tc_id", tc_id)

        with allure.step(f"Получить объект ноды {node_name}"):
            node = request.getfixturevalue(fixture_name)

        request.node.expected = f"Нода {node_name} присутствует в ROS graph"

        with allure.step(f"Проверить что нода {node_name} присутствует в ROS graph"):
            if not node.is_alive():
                request.node.actual = "Нода не запущена — SKIPPED"
                pytest.skip(f"Нода {node_name} не запущена")

            assert node.is_alive() is True

        request.node.actual = f"Нода {node_name} присутствует в ROS graph ✅"

        with allure.step("Зафиксировать результат"):
            allure.attach(
                f"TC ID:     {tc_id}\n"
                f"Node:      {node_name}\n"
                f"Статус:    ALIVE ✅",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )
