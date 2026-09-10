class GeneralIntegrationLocators:

    CAN_TELEMETRY = {
        "node_name":    "/can_telemetry",
        "process_name": "can_telemetry/lib/can_telemetry/can_telemetry_node",
    }
    CARAPI = {
        "node_name":    "/carapi_node",
        "process_name": "carapi_node",
    }
    CLOUD_TELEMETRY = {
        "node_name":    "/infra/cloud_telemetry_node",
        "process_name": "cloud_telemetry/lib/cloud_telemetry/cloud_telemetry_node",
    }
    HARDWARE_METRICS = {
        "node_name":    "/hardware_metrics",
        "process_name": "hardware_metrics/lib/hardware_metrics/hardware_metrics_node",
    }
    METRICS_AGGREGATOR = {
        "node_name":    "/metrics_aggregator",
        "process_name": "metrics_aggregator/lib/metrics_aggregator/metrics_aggregator_node",
    }
    HAL = {
        "node_name":    "/generic/hal",
        "process_name": "generic_hal/lib/generic_hal/generic_hal",
    }
    CRASH_DETECTOR = {
        "node_name":    "/safety/crash_detector",
        "process_name": "crash_detector/lib/crash_detector/crash_detector",
    }
    SDA_PROCESS_MONITOR = {
        "node_name":    "/sda_process_monitor/sda_process_monitor",
        "process_name": "sda_process_monitor/lib/sda_process_monitor/process_monitor_node",
    }
    V2X_PUBLISHER = {
        "node_name":    "/v2x_publisher_node",
        "process_name": "v2x_publisher/lib/v2x_publisher/v2x_publisher",
    }
    ROSBAG2_RECORDER = {
        "node_name":    "/data_logging/rosbag2_recorder",
        "process_name": "sat_infra_rosbag2_transport/lib/sat_infra_rosbag2_transport/rosbag2_recorder_node",
    }
    MRM_ARBITER = {
        "node_name":    "/mrm_arbiter",
        "process_name": "mrm_arbiter/lib/mrm_arbiter/mrm_arbiter_node",
    }
 