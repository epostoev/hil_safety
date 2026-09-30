import pytest
import allure

from framework.kill_fault_injection import run_kill_fault_injection


SENSING_NODES = [
    ("auto_cleaning_node",       "TC-SENSING-PRE-001", "/sensing/auto_cleaning"),
    ("imu1_imu_node",            "TC-SENSING-PRE-002", "/sensing/imu1/imu_node"),
    ("odometry_node",            "TC-SENSING-PRE-003", "/sensing/odometry_node"),
    ("odometry_velocity_node",   "TC-SENSING-PRE-004", "/sensing/odometry_velocity_node"),
    ("radar_driver_node",        "TC-SENSING-PRE-005", "/sensing/radar_driver_node"),
    ("ublox_driver_node",        "TC-SENSING-PRE-006", "/sensing/ublox1/ublox_driver_node"),
    # ("radar_visualization_node","TC-SENSING-PRE-007", "/sensing/visualization/radar_visualization_node"),
    ("roi_selector_node",        "TC-SENSING-PRE-008", "/sensing/roi_selector"),
    # ("camera_decoder_node",    "TC-SENSING-PRE-009", "/sensing/camera_decoder"),
    ("crash_video_recorder_node","TC-SENSING-PRE-010", "/sensing/crash_video_recorder"),
    ("acrux_listener",           "TC-SENSING-PRE-011", "/acrux_listener"),
    ("camera_synchronizer",        "TC-SENSING-PRE-012", "/camera_synchronizer")
]
# /sensing/cloud_builder



class TestSensingKill:

    @pytest.mark.parametrize("fixture_name, tc_id, node_name", SENSING_NODES)
    def test_sensing_kill(self, fixture_name, tc_id, node_name, mrm_monitor, request, restart_autopilot_after):
        node = request.getfixturevalue(fixture_name)
        run_kill_fault_injection(node, node_name, mrm_monitor, request, sla_ms=5000)