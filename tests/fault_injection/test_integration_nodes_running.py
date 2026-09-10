import allure
import pytest


INTEGRATION_NODES = [
    ("can_telemetry_node",       "TC-INT-PRE-001", "/can_telemetry"),
    ("carapi_integration_node",  "TC-INT-PRE-002", "/carapi_node"),
    ("cloud_telemetry_node",     "TC-INT-PRE-003", "/infra/cloud_telemetry_node"),
    ("hardware_metrics_node",    "TC-INT-PRE-004", "/hardware_metrics"),
    ("metrics_aggregator_node",  "TC-INT-PRE-005", "/metrics_aggregator"),
    ("hal_node",                 "TC-INT-PRE-006", "/generic/hal"),
    ("crash_detector_node",      "TC-INT-PRE-007", "/safety/crash_detector"),
    ("sda_process_monitor_node", "TC-INT-PRE-008", "/sda_process_monitor/sda_process_monitor"),
    ("v2x_publisher_node",       "TC-INT-PRE-009", "/v2x_publisher_node"),
    # ("rosbag2_recorder_node",    "TC-INT-PRE-010", "/data_logging/rosbag2_recorder"),
    # ("mrm_arbiter_node",         "TC-INT-PRE-011", "/mrm_arbiter"),
]


class TestIntegrationNodesRunning:

    @pytest.mark.parametrize("fixture_name, tc_id, node_name", INTEGRATION_NODES)
    def test_node_running(self, fixture_name, tc_id, node_name, request):
        f"""{tc_id}: {node_name} присутствует в ROS graph"""

        node = request.getfixturevalue(fixture_name)

        request.node.expected = f"Нода {node_name} присутствует в ROS graph"

        if not node.is_alive():
            request.node.actual = "Нода не запущена — SKIPPED"
            pytest.skip(f"Нода {node_name} не запущена")

        assert node.is_alive() is True

        request.node.actual = f"Нода {node_name} жива ✅"