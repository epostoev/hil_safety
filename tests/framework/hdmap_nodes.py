from framework.base_hil_test import BaseHILTest


class HdmapServiceNode(BaseHILTest):
    NODE_NAME = "/hdmap_service_node"
    PROCESS_NAME = "hdmap_service/lib/hdmap_service/hdmap_service_node"

    def __init__(self):
        super().__init__(node_name="hdmap_service_node", timeout=15)


class DynamicObjectsServiceNode(BaseHILTest):
    NODE_NAME = "/dynamic_objects_service_node"
    PROCESS_NAME = "dynamic_objects_service/lib/dynamic_objects_service/dynamic_objects_service_node"

    def __init__(self):
        super().__init__(node_name="dynamic_objects_service_node", timeout=15)


class RtkProviderNode(BaseHILTest):
    NODE_NAME = "/rtk_provider_node"
    PROCESS_NAME = "rtk_provider/lib/rtk_provider/rtk_provider_node"

    def __init__(self):
        super().__init__(node_name="rtk_provider_node", timeout=15)


class HdmapVisualizationNode(BaseHILTest):
    NODE_NAME = "/hdmap/visualization/hdmap_visualization_node"
    PROCESS_NAME = "hdmap_visualization/lib/hdmap_visualization/hdmap_visualization_node"

    def __init__(self):
        super().__init__(node_name="hdmap_visualization_node", timeout=15)


# Нода не найдена в ps aux — PROCESS_NAME уточнить
class HdmapIssueReporterNode(BaseHILTest):
    NODE_NAME = "/hdmap/issue_reporter"
    PROCESS_NAME = "issue_reporter"  # уточнить через ps aux

    def __init__(self):
        super().__init__(node_name="issue_reporter", timeout=15)
