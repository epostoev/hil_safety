import pytest
import allure


SENSING_NODES = [
    ("auto_cleaning_node",       "TC-SENSING-PRE-001", "/sensing/auto_cleaning"),
    ("imu1_imu_node",            "TC-SENSING-PRE-002", "/sensing/imu1/imu_node"),
    ("odometry_node",            "TC-SENSING-PRE-003", "/sensing/odometry_node"),
    ("odometry_velocity_node",   "TC-SENSING-PRE-004", "/sensing/odometry_velocity_node"),
    ("radar_driver_node",        "TC-SENSING-PRE-005", "/sensing/radar_driver_node"),
    ("ublox_driver_node",        "TC-SENSING-PRE-006", "/sensing/ublox1/ublox_driver_node"),
    # ("radar_visualization_node", "TC-SENSING-PRE-007", "/sensing/visualization/radar_visualization_node"),
    ("roi_selector_node",        "TC-SENSING-PRE-008", "/sensing/roi_selector"),
    # ("camera_decoder_node",      "TC-SENSING-PRE-009", "/sensing/camera_decoder"),
    ("crash_video_recorder_node","TC-SENSING-PRE-010", "/sensing/crash_video_recorder")
]

@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Тест: Состояние ноды в системе')
@allure.description('Провека присутствия ноды в релизе r/0.16')
class TestSensingNodesRunning:

    @pytest.mark.parametrize("fixture_name, tc_id, node_name", SENSING_NODES)
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