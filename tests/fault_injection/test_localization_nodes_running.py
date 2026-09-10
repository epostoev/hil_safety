import pytest


LOCALIZATION_NODES = [
    ("localization_output_gateway_node",   "TC-LOC-PRE-001", "/localization_output_gateway_node"),
    ("localization_node_container_node",   "TC-LOC-PRE-002", "/localization/node_container"),
]

class TestLocalizationNodesRunning:

    @pytest.mark.parametrize("fixture_name, tc_id, node_name", LOCALIZATION_NODES)
    def test_node_running(self, fixture_name, tc_id, node_name, request):
        f"""{tc_id}: {node_name} присутствует в ROS graph"""

        node = request.getfixturevalue(fixture_name)

        request.node.expected = f"Нода {node_name} присутствует в ROS graph"

        if not node.is_alive():
            request.node.actual = "Нода не запущена — SKIPPED"
            pytest.skip(f"Нода {node_name} не запущена")

        assert node.is_alive() is True

        request.node.actual = f"Нода {node_name} жива ✅"