from framework.base_hil_test import BaseHILTest


class LocalizationOutputGatewayNode(BaseHILTest):
    NODE_NAME = "/localization_output_gateway_node"
    PROCESS_NAME = "localization/lib/localization/localization_output_gateway_node"

    def __init__(self):
        super().__init__(node_name="/localization_output_gateway_node", timeout=15)


class LocalizationNodeContainerNode(BaseHILTest):
    NODE_NAME = "/localization/node_container"
    PROCESS_NAME = "sat_utils_node_container/lib/sat_utils_node_container/node_container"

    def __init__(self):
        super().__init__(node_name="/localization/node_container", timeout=15)
