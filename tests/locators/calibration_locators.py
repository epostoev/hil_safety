class CalibrationLocators:

    INTRINSIC_PUBLISHER = {
        "node_name":    "/intrinsic_publisher",
        "process_name": "intrinsic_camera_calibration/lib/intrinsic_camera_calibration/intrinsic_publisher",
    }
    CAMERA_TO_BASELINK_ONLINE_CALIBRATOR = {
        "node_name":    "/calibration/rct/camera_to_baselink_online_calibrator",
        "process_name": "camera_to_baselink_online_calibrator/lib/camera_to_baselink_online_calibrator/camera_to_baselink_online_calibrator",
    }
    IMU_BASELINK_RUNTIME_CALIBRATION = {
        "node_name":    "/calibration/rct/imu/imu_baselink_runtime_calibration",
        "process_name": "imu_baselink_runtime_calibration/lib/imu_baselink_runtime_calibration/imu_baselink_runtime_calibration",
    }
    RUNTIME_RADAR_AUTOCALIBRATION = {
        "node_name":    "/calibration/rct/runtime_radar_autocalibration",
        "process_name": "runtime_radar_autocalibration/lib/runtime_radar_autocalibration/runtime_radar_autocalibration",
    }
    CAM_TO_CAM_TF_ESTIMATORS = {
        "node_name":    "/calibration/rct/cam_to_cam_tf_estimators",
        "process_name": "__node:=tf_estimation_node",
    }
    FEATURE_EXTRACTORS = {
        "node_name":    "/calibration/rct/feature_extractors",
        "process_name": "__node:=synced_feature_extractor",
    }
    CAM_TO_CAM_CONTROLLER = {
        "node_name":    "/calibration/rct/cam_to_cam_controller",
        "process_name": "cam_to_cam_controller/lib/cam_to_cam_controller/cam_to_cam_controller",
    }
    RCT_VALIDATOR = {
        "node_name":    "/calibration/rct/rct_validator",
        "process_name": "rct_validator/lib/rct_validator/rct_validator",
    }
    ROBOT_STATE_PUBLISHER = {
        "node_name":    "/robot_state_publisher",
        "process_name": "robot_state_publisher/robot_state_publisher",
    }