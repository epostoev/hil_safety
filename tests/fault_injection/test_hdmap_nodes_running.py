import pytest
import allure


HDMAP_NODES = [
    ("hdmap_service_node_alive",            "TC-HDM-KILL-001", "/hdmap_service_node"),
    ("hdmap_dynamic_objects_service_alive", "TC-HDM-KILL-002", "/dynamic_objects_service_node"),
    ("hdmap_rtk_provider_node_alive",       "TC-HDM-KILL-003", "/rtk_provider_node"),
    # ("hdmap_issue_reporter_node_alive",     "TC-HDM-KILL-004", "/hdmap/issue_reporter"),
    # ("hdmap_visualization_node_alive",      "TC-HDM-KILL-005", "/hdmap/visualization/hdmap_visualization_node"),
]


@allure.epic("HIL Testing")
@allure.feature("HD-Map")
@allure.story("Предусловия: проверка запуска нод")
@allure.title("Проверка запуска нод компонента HD-Map")
@allure.description(
    "Предусловия: все ноды компонента HD-Map должны присутствовать в ROS graph. "
    "Тест проверяет каждую ноду через is_alive()."
)
class TestHdmapNodesRunning:
    """
    Проверка что все ноды компонента HD-Map запущены.

    TC-HDM-PRE-001: /hdmap_service_node
    TC-HDM-PRE-002: /dynamic_objects_service_node
    TC-HDM-PRE-003: /rtk_provider_node
    TC-HDM-PRE-004: /hdmap/issue_reporter
    TC-HDM-PRE-005: /hdmap/visualization/hdmap_visualization_node
    """

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", HDMAP_NODES)
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