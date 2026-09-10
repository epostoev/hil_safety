class HdmapLocators:
 
    HDMAP_SERVICE = {
        "node_name":    "/hdmap_service_node",
        "process_name": "hdmap_service/lib/hdmap_service/hdmap_service_node",
    }
    DYNAMIC_OBJECTS_SERVICE = {
        "node_name":    "/dynamic_objects_service_node",
        "process_name": "dynamic_objects_service/lib/dynamic_objects_service/dynamic_objects_service_node",
    }
    RTK_PROVIDER = {
        "node_name":    "/rtk_provider_node",
        "process_name": "rtk_provider/lib/rtk_provider/rtk_provider_node",
    }
    HDMAP_VISUALIZATION = {
        "node_name":    "/hdmap/visualization/hdmap_visualization_node",
        "process_name": "hdmap_visualization/lib/hdmap_visualization/hdmap_visualization_node",
    }
    ISSUE_REPORTER = {
        "node_name":    "/hdmap/issue_reporter",
        "process_name": "issue_reporter",  # уточнить через ps aux
    }
 