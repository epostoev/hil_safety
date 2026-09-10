from framework.base_hil_test import BaseHILTest


class IntrinsicPublisherNode(BaseHILTest):
    NODE_NAME = "/intrinsic_publisher"
    PROCESS_NAME = "intrinsic_camera_calibration/lib/intrinsic_camera_calibration/intrinsic_publisher"

    def __init__(self):
        super().__init__(node_name="intrinsic_publisher", timeout=15)


class CameraToBaselinkOnlineCalibratorNode(BaseHILTest):
    NODE_NAME = "/calibration/rct/camera_to_baselink_online_calibrator"
    PROCESS_NAME = "camera_to_baselink_online_calibrator/lib/camera_to_baselink_online_calibrator/camera_to_baselink_online_calibrator"

    def __init__(self):
        super().__init__(node_name="camera_to_baselink_online_calibrator", timeout=15)


class ImuBaselinkRuntimeCalibrationNode(BaseHILTest):
    NODE_NAME = "/calibration/rct/imu/imu_baselink_runtime_calibration"
    PROCESS_NAME = "imu_baselink_runtime_calibration/lib/imu_baselink_runtime_calibration/imu_baselink_runtime_calibration"

    def __init__(self):
        super().__init__(node_name="imu_baselink_runtime_calibration", timeout=15)


class RuntimeRadarAutocalibrationNode(BaseHILTest):
    NODE_NAME = "/calibration/rct/runtime_radar_autocalibration"
    PROCESS_NAME = "runtime_radar_autocalibration/lib/runtime_radar_autocalibration/runtime_radar_autocalibration"

    def __init__(self):
        super().__init__(node_name="runtime_radar_autocalibration", timeout=15)


class CamToCamTfEstimatorsNode(BaseHILTest):
    # Бинарник переименован через __node:=tf_estimation_node
    NODE_NAME = "/calibration/rct/cam_to_cam_tf_estimators"
    PROCESS_NAME = "__node:=tf_estimation_node"

    def __init__(self):
        super().__init__(node_name="cam_to_cam_tf_estimators", timeout=15)


class FeatureExtractorsNode(BaseHILTest):
    # Бинарник переименован через __node:=synced_feature_extractor
    NODE_NAME = "/calibration/rct/feature_extractors"
    PROCESS_NAME = "__node:=synced_feature_extractor"

    def __init__(self):
        super().__init__(node_name="feature_extractors", timeout=15)


class CamToCamControllerNode(BaseHILTest):
    NODE_NAME = "/calibration/rct/cam_to_cam_controller"
    PROCESS_NAME = "cam_to_cam_controller/lib/cam_to_cam_controller/cam_to_cam_controller"

    def __init__(self):
        super().__init__(node_name="cam_to_cam_controller", timeout=15)


class RctValidatorNode(BaseHILTest):
    NODE_NAME = "/calibration/rct/rct_validator"
    PROCESS_NAME = "rct_validator/lib/rct_validator/rct_validator"

    def __init__(self):
        super().__init__(node_name="rct_validator", timeout=15)


class RobotStatePublisherNode(BaseHILTest):
    # Стандартная ROS2 нода из /opt/ros/humble/
    NODE_NAME = "/robot_state_publisher"
    PROCESS_NAME = "robot_state_publisher/robot_state_publisher"

    def __init__(self):
        super().__init__(node_name="robot_state_publisher", timeout=15)
