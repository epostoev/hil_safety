import pytest
import allure

from framework.kill_fault_injection import run_kill_fault_injection


CALIBRATION_NODES = [
    # ("calibration_intrinsic_publisher_node",                    "TC-CAL-PRE-001", "/intrinsic_publisher"),
    ("calibration_camera_to_baselink_online_calibrator_node",   "TC-CAL-PRE-002", "/calibration/rct/camera_to_baselink_online_calibrator"),
    ("calibration_imu_baselink_runtime_calibration_node",       "TC-CAL-PRE-003", "/calibration/rct/imu/imu_baselink_runtime_calibration"),
    ("calibration_runtime_radar_autocalibration_node",          "TC-CAL-PRE-004", "/calibration/rct/runtime_radar_autocalibration"),
    # ("calibration_cam_to_cam_tf_estimators_node",               "TC-CAL-PRE-005", "/calibration/rct/cam_to_cam_tf_estimators"),
    # ("calibration_feature_extractors_node",                     "TC-CAL-PRE-006", "/calibration/rct/feature_extractors"),
    ("calibration_cam_to_cam_controller_node",                  "TC-CAL-PRE-007", "/calibration/rct/cam_to_cam_controller"),
    ("calibration_rct_validator_node",                          "TC-CAL-PRE-008", "/calibration/rct/rct_validator"),
    # ("calibration_robot_state_publisher_node",                  "TC-CAL-PRE-009", "/robot_state_publisher"),
]


@allure.epic("HIL Testing")
@allure.feature("Calibration")
@allure.story("Fault Injection: kill -6 нод")
@allure.title("Fault Injection: принудительное завершение нод компонента Calibration")
@allure.description(
    "Тест отправляет kill -6 каждой ноде компонента Calibration "
    "и проверяет что MRM реагирует переходом mrm_type: 0 → 2 "
    "в течение 5000ms."
)
class TestCalibrationKill:
    """
    Fault Injection: принудительное завершение нод компонента Calibration.

    TC-CAL-KILL-001: /intrinsic_publisher
    TC-CAL-KILL-002: /calibration/rct/camera_to_baselink_online_calibrator
    TC-CAL-KILL-003: /calibration/rct/imu/imu_baselink_runtime_calibration
    TC-CAL-KILL-004: /calibration/rct/runtime_radar_autocalibration
    TC-CAL-KILL-005: /calibration/rct/cam_to_cam_tf_estimators
    TC-CAL-KILL-006: /calibration/rct/feature_extractors
    TC-CAL-KILL-007: /calibration/rct/cam_to_cam_controller
    TC-CAL-KILL-008: /calibration/rct/rct_validator
    TC-CAL-KILL-009: /robot_state_publisher
    TC-CAL-KILL-010: /intrinsic_repair_service
    TC-CAL-KILL-011: /calibration/calapi_node
    """

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", CALIBRATION_NODES)
    def test_calibration_kill(self, fixture_name, tc_id, node_name,
                              mrm_monitor, request, restart_autopilot_after):

        allure.dynamic.title(f"{tc_id}: kill -6 {node_name}")
        allure.dynamic.parameter("node_name", node_name)
        allure.dynamic.parameter("tc_id", tc_id)

        with allure.step(f"Получить объект ноды {node_name}"):
            node = request.getfixturevalue(fixture_name)

        run_kill_fault_injection(node, node_name, mrm_monitor, request, sla_ms=5000)