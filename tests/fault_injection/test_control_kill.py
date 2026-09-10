import pytest
import allure

from framework.kill_fault_injection import run_kill_fault_injection


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
@allure.story("Fault Injection: kill -6 нод")
@allure.title("Fault Injection: принудительное завершение нод компонента Control")
@allure.description(
    "Тест отправляет kill -6 каждой ноде компонента Control "
    "и проверяет что MRM реагирует переходом mrm_type: 0 → 2 "
    "в течение 5000ms."
)
class TestControlKill:
    """
    Fault Injection: принудительное завершение нод компонента Control.

    TC-CTL-KILL-001: /chassis/chassis_bridge_udp_reader
    TC-CTL-KILL-002: /chassis/rover_feedback
    TC-CTL-KILL-003: /chassis/chassis_adapter_sender
    TC-CTL-KILL-004: /chassis/chassis_adapter_receiver
    TC-CTL-KILL-005: /control/input_monitor
    TC-CTL-KILL-006: /control/mpc
    TC-CTL-KILL-007: /chassis/telecan_body
    TC-CTL-KILL-008: /chassis/safety_traffic_analyzer
    """

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", CONTROL_NODES)
    def test_control_kill(self, fixture_name, tc_id, node_name,
                          mrm_monitor, request, restart_autopilot_after):

        allure.dynamic.title(f"{tc_id}: kill -6 {node_name}")
        allure.dynamic.parameter("node_name", node_name)
        allure.dynamic.parameter("tc_id", tc_id)

        with allure.step(f"Получить объект ноды {node_name}"):
            node = request.getfixturevalue(fixture_name)

        run_kill_fault_injection(node, node_name, mrm_monitor, request, sla_ms=5000)