from framework.base_hil_test import BaseHILTest


class CanTelemetryNode(BaseHILTest):
    NODE_NAME = "/can_telemetry"
    PROCESS_NAME = "can_telemetry/lib/can_telemetry/can_telemetry_node"

    def __init__(self):
        super().__init__(node_name="can_telemetry", timeout=15)


class CarapiNode(BaseHILTest):
    NODE_NAME = "/carapi_node"
    PROCESS_NAME = "carapi_node"

    def __init__(self):
        super().__init__(node_name="carapi_node", timeout=15)


class CloudTelemetryNode(BaseHILTest):
    NODE_NAME = "/infra/cloud_telemetry_node"
    PROCESS_NAME = "cloud_telemetry/lib/cloud_telemetry/cloud_telemetry_node"

    def __init__(self):
        super().__init__(node_name="cloud_telemetry_node", timeout=15)


class HardwareMetricsNode(BaseHILTest):
    NODE_NAME = "/hardware_metrics"
    PROCESS_NAME = "hardware_metrics/lib/hardware_metrics/hardware_metrics_node"

    def __init__(self):
        super().__init__(node_name="hardware_metrics", timeout=15)


class MetricsAggregatorNode(BaseHILTest):
    NODE_NAME = "/metrics_aggregator"
    PROCESS_NAME = "metrics_aggregator/lib/metrics_aggregator/metrics_aggregator_node"

    def __init__(self):
        super().__init__(node_name="metrics_aggregator", timeout=15)


class HalNode(BaseHILTest):
    NODE_NAME = "/generic/hal"
    PROCESS_NAME = "generic_hal/lib/generic_hal/generic_hal"

    def __init__(self):
        super().__init__(node_name="/generic/hal", timeout=15)


class CrashDetectorNode(BaseHILTest):
    NODE_NAME = "/safety/crash_detector"
    PROCESS_NAME = "crash_detector/lib/crash_detector/crash_detector"

    def __init__(self):
        super().__init__(node_name="/safety/crash_detector", timeout=15)


class SdaProcessMonitorNode(BaseHILTest):
    NODE_NAME = "/sda_process_monitor/sda_process_monitor"
    PROCESS_NAME = "sda_process_monitor/lib/sda_process_monitor/process_monitor_node"

    def __init__(self):
        super().__init__(node_name="/sda_process_monitor/sda_process_monitor", timeout=15)


class V2xPublisherNode(BaseHILTest):
    NODE_NAME = "/v2x_publisher_node"
    PROCESS_NAME = "v2x_publisher/lib/v2x_publisher/v2x_publisher"

    def __init__(self):
        super().__init__(node_name="/v2x_publisher_node", timeout=15)


class Rosbag2RecorderNode(BaseHILTest):
    NODE_NAME = "/data_logging/rosbag2_recorder"
    PROCESS_NAME = "sat_infra_rosbag2_transport/lib/sat_infra_rosbag2_transport/rosbag2_recorder_node"

    def __init__(self):
        super().__init__(node_name="/data_logging/rosbag2_recorder", timeout=15)


class MrmArbiterNode(BaseHILTest):
    NODE_NAME = "/mrm_arbiter"
    PROCESS_NAME = "mrm_arbiter/lib/mrm_arbiter/mrm_arbiter_node"

    def __init__(self):
        super().__init__(node_name="/mrm_arbiter", timeout=15)
