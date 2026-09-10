class SensingLocators:

    AUTO_CLEANING = {
        "node_name":    "/sensing/auto_cleaning",
        "process_name": "auto_cleaning/lib/auto_cleaning/auto_cleaning_node",
    }
    IMU = {
        "node_name":    "/sensing/imu1/imu_node",
        "process_name": "imu_driver/lib/imu_driver/imu_node",
    }
    ODOMETRY = {
        "node_name":    "/sensing/odometry_node",
        "process_name": "odometry_driver/lib/odometry_driver/odometry_node",
    }
    ODOMETRY_VELOCITY = {
        "node_name":    "/sensing/odometry_velocity_node",
        "process_name": "odometry_velocity/lib/odometry_velocity/odometry_velocity_node",
    }
    RADAR_DRIVER = {
        "node_name":    "/sensing/radar_driver_node",
        "process_name": "radar_driver/lib/radar_driver/radar_driver_node",
    }
    UBLOX_DRIVER = {
        "node_name":    "/sensing/ublox1/ublox_driver_node",
        "process_name": "ublox_driver/lib/ublox_driver/ublox_driver_node",
    }
    RADAR_VISUALIZATION = {
        "node_name":    "/sensing/visualization/radar_visualization_node",
        "process_name": "radar_visualization/lib/radar_visualization/radar_visualization_node",
    }
    ROI_SELECTOR = {
        "node_name":    "/sensing/roi_selector",
        "process_name": "roi_selector/lib/roi_selector/roi_selector",
    }
    CAMERA_DECODER = {
        "node_name":    "/sensing/camera_decoder",
        "process_name": "sat_sensing_camera_decoder/lib/sat_sensing_camera_decoder/camera_decoder_node",
    }
    CRASH_VIDEO_RECORDER = {
        "node_name":    "/sensing/crash_video_recorder",
        "process_name": "crash_video_recorder/lib/crash_video_recorder/crash_video_recorder_node",
    }