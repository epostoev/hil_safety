import pytest
import allure

from framework.kill_fault_injection import run_kill_fault_injection


LOCALIZATION_NODES = [
    ("localization_output_gateway_node",   "TC-LOC-PRE-001", "/localization_output_gateway_node"),
    ("localization_node_container_node",   "TC-LOC-PRE-002", "/localization/node_container"),
]


class TestLocalizationKill:

    @pytest.mark.parametrize("fixture_name, tc_id, node_name", LOCALIZATION_NODES)
    def test_localization_kill(self, fixture_name, tc_id, node_name,
                               mrm_monitor, request, restart_autopilot_after):
        node = request.getfixturevalue(fixture_name)
        run_kill_fault_injection(node, node_name, mrm_monitor, request, sla_ms=5000)