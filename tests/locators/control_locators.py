class ControlLocators:

    CHASSIS_BRIDGE_UDP_READER = {
        "node_name":    "/chassis/chassis_bridge_udp_reader",
        "process_name": "chassis_bridge/lib/chassis_bridge/chassis_bridge_udp_reader",
    }
    ROVER_FEEDBACK = {
        "node_name":    "/chassis/rover_feedback",
        "process_name": "rover_feedback/lib/rover_feedback/rover_feedback_node",
    }
    CHASSIS_ADAPTER_SENDER = {
        "node_name":    "/chassis/chassis_adapter_sender",
        "process_name": "chassis_adapter/lib/chassis_adapter/chassis_adapter_sender",
    }
    CHASSIS_ADAPTER_RECEIVER = {
        "node_name":    "/chassis/chassis_adapter_receiver",
        "process_name": "chassis_adapter/lib/chassis_adapter/chassis_adapter_receiver",
    }
    INPUT_MONITOR = {
        "node_name":    "/control/input_monitor",
        "process_name": "control_input_monitor/lib/control_input_monitor/control_input_monitor",
    }
    MPC = {
        "node_name":    "/control/mpc",
        "process_name": "mpc/lib/mpc/mpc",
    }
    TELECAN_BODY = {
        "node_name":    "/chassis/telecan_body",
        "process_name": "telecan_body",  # уточнить через ps aux
    }
    SAFETY_TRAFFIC_ANALYZER = {
        "node_name":    "/chassis/safety_traffic_analyzer",
        "process_name": "safety_traffic_analyzer",  # уточнить через ps aux
    }