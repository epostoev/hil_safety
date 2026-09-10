from framework.base_hil_test import BaseHILTest


class AutoCleaningNode(BaseHILTest):
    NODE_NAME = "/sensing/auto_cleaning"
    PROCESS_NAME = "auto_cleaning/lib/auto_cleaning/auto_cleaning_node"

    def __init__(self):
        super().__init__(node_name="auto_cleaning", timeout=15)


class ImuNode(BaseHILTest):
    NODE_NAME = "/sensing/imu1/imu_node"
    PROCESS_NAME = "imu_driver/lib/imu_driver/imu_node"

    def __init__(self):
        super().__init__(node_name="imu_node", timeout=15)


class OdometryNode(BaseHILTest):
    NODE_NAME = "/sensing/odometry_node"
    PROCESS_NAME = "odometry_driver/lib/odometry_driver/odometry_node"

    def __init__(self):
        super().__init__(node_name="odometry_node", timeout=15)


class OdometryVelocityNode(BaseHILTest):
    NODE_NAME = "/sensing/odometry_velocity_node"
    PROCESS_NAME = "odometry_velocity/lib/odometry_velocity/odometry_velocity_node"

    def __init__(self):
        super().__init__(node_name="odometry_velocity_node", timeout=15)


class RadarDriverNode(BaseHILTest):
    NODE_NAME = "/sensing/radar_driver_node"
    PROCESS_NAME = "radar_driver/lib/radar_driver/radar_driver_node"

    def __init__(self):
        super().__init__(node_name="radar_driver_node", timeout=15)


class UbloxDriverNode(BaseHILTest):
    NODE_NAME = "/sensing/ublox1/ublox_driver_node"
    PROCESS_NAME = "ublox_driver/lib/ublox_driver/ublox_driver_node"

    def __init__(self):
        super().__init__(node_name="ublox_driver_node", timeout=15)


class RadarVisualizationNode(BaseHILTest):
    NODE_NAME = "/sensing/visualization/radar_visualization_node"
    PROCESS_NAME = "radar_visualization/lib/radar_visualization/radar_visualization_node"

    def __init__(self):
        super().__init__(node_name="radar_visualization_node", timeout=15)


class RoiSelectorNode(BaseHILTest):
    NODE_NAME = "/sensing/roi_selector"
    PROCESS_NAME = "roi_selector/lib/roi_selector/roi_selector"

    def __init__(self):
        super().__init__(node_name="roi_selector", timeout=15)


class CameraDecoderNode(BaseHILTest):
    NODE_NAME = "/sensing/camera_decoder"
    PROCESS_NAME = "sat_sensing_camera_decoder/lib/sat_sensing_camera_decoder/camera_decoder_node"

    def __init__(self):
        super().__init__(node_name="camera_decoder", timeout=15)


class CrashVideoRecorderNode(BaseHILTest):
    NODE_NAME = "/sensing/crash_video_recorder"
    PROCESS_NAME = "crash_video_recorder/lib/crash_video_recorder/crash_video_recorder_node"

    def __init__(self):
        super().__init__(node_name="crash_video_recorder", timeout=15)
