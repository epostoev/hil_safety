from framework.base_hil_test import BaseHILTest


class ChassisBridgeUdpReaderNode(BaseHILTest):
    NODE_NAME = "/chassis/chassis_bridge_udp_reader"
    PROCESS_NAME = "chassis_bridge/lib/chassis_bridge/chassis_bridge_udp_reader"

    def __init__(self):
        super().__init__(node_name="chassis_bridge_udp_reader", timeout=15)


class RoverFeedbackNode(BaseHILTest):
    NODE_NAME = "/chassis/rover_feedback"
    PROCESS_NAME = "rover_feedback/lib/rover_feedback/rover_feedback_node"

    def __init__(self):
        super().__init__(node_name="rover_feedback", timeout=15)


class ChassisAdapterSenderNode(BaseHILTest):
    NODE_NAME = "/chassis/chassis_adapter_sender"
    PROCESS_NAME = "chassis_adapter/lib/chassis_adapter/chassis_adapter_sender"

    def __init__(self):
        super().__init__(node_name="chassis_adapter_sender", timeout=15)


class ChassisAdapterReceiverNode(BaseHILTest):
    NODE_NAME = "/chassis/chassis_adapter_receiver"
    PROCESS_NAME = "chassis_adapter/lib/chassis_adapter/chassis_adapter_receiver"

    def __init__(self):
        super().__init__(node_name="chassis_adapter_receiver", timeout=15)


class ControlInputMonitorNode(BaseHILTest):
    NODE_NAME = "/control/input_monitor"
    PROCESS_NAME = "control_input_monitor/lib/control_input_monitor/control_input_monitor"

    def __init__(self):
        super().__init__(node_name="input_monitor", timeout=15)


class MpcNode(BaseHILTest):
    NODE_NAME = "/control/mpc"
    PROCESS_NAME = "mpc/lib/mpc/mpc"

    def __init__(self):
        super().__init__(node_name="mpc", timeout=15)


# Ноды не найденные в ps aux — не запущены на текущем стенде
# PROCESS_NAME уточнить когда ноды будут активны

class TelecanBodyNode(BaseHILTest):
    NODE_NAME = "/chassis/telecan_body"
    PROCESS_NAME = "telecan_body"  # уточнить через ps aux

    def __init__(self):
        super().__init__(node_name="telecan_body", timeout=15)


class SafetyTrafficAnalyzerNode(BaseHILTest):
    NODE_NAME = "/chassis/safety_traffic_analyzer"
    PROCESS_NAME = "safety_traffic_analyzer"  # уточнить через ps aux

    def __init__(self):
        super().__init__(node_name="safety_traffic_analyzer", timeout=15)
