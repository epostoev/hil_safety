import pytest
import allure


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
@allure.story("Предусловия: проверка запуска нод")
@allure.title("Проверка запуска нод компонента Calibration")
@allure.description(
    "Предусловия: все ноды компонента Calibration должны присутствовать в ROS graph. "
    "Тест проверяет каждую ноду через is_alive()."
)
class TestCalibrationNodesRunning:
    """
    Проверка что все ноды компонента Calibration запущены.

    TC-CAL-PRE-001: /intrinsic_publisher
    TC-CAL-PRE-002: /calibration/rct/camera_to_baselink_online_calibrator
    TC-CAL-PRE-003: /calibration/rct/imu/imu_baselink_runtime_calibration
    TC-CAL-PRE-004: /calibration/rct/runtime_radar_autocalibration
    TC-CAL-PRE-005: /calibration/rct/cam_to_cam_tf_estimators
    TC-CAL-PRE-006: /calibration/rct/feature_extractors
    TC-CAL-PRE-007: /calibration/rct/cam_to_cam_controller
    TC-CAL-PRE-008: /calibration/rct/rct_validator
    TC-CAL-PRE-009: /robot_state_publisher
    TC-CAL-PRE-010: /intrinsic_repair_service
    TC-CAL-PRE-011: /calibration/calapi_node
    """

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", CALIBRATION_NODES)
    def test_node_running(self, fixture_name, tc_id, node_name,
                          node_alive_factory, request):
        f"""{tc_id}: {node_name} присутствует в ROS graph"""

        allure.dynamic.title(f"{tc_id}: {node_name}")
        allure.dynamic.parameter("node_name", node_name)
        allure.dynamic.parameter("tc_id", tc_id)
        with allure.step(f"Получить объект ноды {node_name}"):
            node = node_alive_factory(fixture_name)
        request.node.expected = f"Нода {node_name} присутствует в ROS graph"
        with allure.step(f"Проверить что нода {node_name} присутствует в ROS graph"):
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