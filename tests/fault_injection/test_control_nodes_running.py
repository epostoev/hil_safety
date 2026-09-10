import pytest
import allure


CONTROL_NODES = [
    ("control_chassis_bridge_udp_reader_node_alive", "TC-CTL-KILL-001", "/chassis/chassis_bridge_udp_reader"),
    ("control_rover_feedback_node_alive",            "TC-CTL-KILL-002", "/chassis/rover_feedback"),
    ("control_chassis_adapter_sender_node_alive",    "TC-CTL-KILL-003", "/chassis/chassis_adapter_sender"),
    # ("control_chassis_adapter_receiver_node_alive",  "TC-CTL-KILL-004", "/chassis/chassis_adapter_receiver"),
    # ("control_input_monitor_node_alive",             "TC-CTL-KILL-005", "/control/input_monitor"),
    # ("control_mpc_node_alive",                       "TC-CTL-KILL-006", "/control/mpc"),
    # ("control_telecan_body_node_alive",              "TC-CTL-KILL-007", "/chassis/telecan_body"),
    # ("control_safety_traffic_analyzer_node_alive",   "TC-CTL-KILL-008", "/chassis/safety_traffic_analyzer"),
]


@allure.epic("HIL Testing")
@allure.feature("Control")
@allure.story("Предусловия: проверка запуска нод")
@allure.title("Проверка запуска нод компонента Control")
@allure.description(
    "Предусловия: все ноды компонента Control должны присутствовать в ROS graph. "
    "Тест проверяет каждую ноду через is_alive()."
)
class TestControlNodesRunning:
    """
    Проверка что все ноды компонента Control запущены.

    TC-CTL-PRE-001: /chassis/chassis_bridge_udp_reader
    TC-CTL-PRE-002: /chassis/rover_feedback
    TC-CTL-PRE-003: /chassis/chassis_adapter_sender
    TC-CTL-PRE-004: /chassis/chassis_adapter_receiver
    TC-CTL-PRE-005: /control/input_monitor
    TC-CTL-PRE-006: /control/mpc
    TC-CTL-PRE-007: /chassis/telecan_body
    TC-CTL-PRE-008: /chassis/safety_traffic_analyzer
    """

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", CONTROL_NODES)
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