class PerceptionLocators:

    BOOM_BARRIER_DETECTOR = {
        "node_name":    "/perception/boom_barrier_detector",
        "process_name": "sat_perception_boom_barrier_detector/lib/sat_perception_boom_barrier_detector/boom_barrier_detector_node",
    }
    BOX_SEGMENTATION_FUSION = {
        "node_name":    "/perception/box_segmentation_fusion",
        "process_name": "sat_perception_box_segmentation_fusion/lib/sat_perception_box_segmentation_fusion/box_segmentation_fusion_node",
    }
    CAMERA_DETECTS_FUSING = {
        "node_name":    "/perception/camera_detects_fusing",
        "process_name": "camera_detects_fusing/lib/camera_detects_fusing/camera_detects_fusing",
    }
    CAMERA_MAP_DETECTOR = {
        "node_name":    "/perception/camera_map_detector",
        "process_name": "camera_map_detector/lib/camera_map_detector/camera_map_detector",
    }
    CAMERA_TRACKER_CPP = {
        "node_name":    "/perception/camera_tracker_cpp",
        "process_name": "camera_tracker_cpp/lib/camera_tracker_cpp/camera_tracker_cpp",
    }
    CAMERA_TRACKS_MERGER = {
        "node_name":    "/perception/camera_tracks_merger",
        "process_name": "camera_tracks_merger/lib/camera_tracks_merger/camera_tracks_merger",
    }
    CLOUD_MOTION_DETECTOR = {
        "node_name":    "/perception/cloud_motion_detector",
        "process_name": "cloud_motion_detector/lib/cloud_motion_detector/cloud_motion_detector",
    }
    DETECTOR_3D = {
        "node_name":    "/perception/detector_3d",
        "process_name": "detector_3d/lib/detector_3d/detector_3d",
    }
    FRONT_BACKBONE = {
        "node_name":    "/perception/front_backbone",
        "process_name": "front_backbone/lib/front_backbone/front_backbone",
    }
    IMAGE_SEGMENTER = {
        "node_name":    "/perception/image_segmenter_cpp",
        "process_name": "sat_perception_image_segmenter_cpp/lib/sat_perception_image_segmenter_cpp/image_segmenter_cpp_node",
    }
    LIDAR_BLIND_ZONES = {
        "node_name":    "/perception/lidar_blind_zones",
        "process_name": "lidar_blind_zones/lib/lidar_blind_zones/lidar_blind_zones",
    }
    LIDAR_NOISE_DETECTOR = {
        "node_name":    "/perception/lidar_noise_detector",
        "process_name": "sat_perception_lidar_noise_detector/lib/sat_perception_lidar_noise_detector/lidar_noise_detector_node",
    }
    STATIC_OBSTACLES_TRACKER = {
        "node_name":    "/perception/static_obstacles_tracker",
        "process_name": "sat_perception_static_obstacles_tracker/static_obstacles_tracker_node",
    }
    POINT_CLOUD_CLUSTERIZER = {
        "node_name":    "/perception/point_cloud_clusterizer",
        "process_name": "point_cloud_clusterizer/lib/point_cloud_clusterizer/point_cloud_clusterizer",
    }
    POLLUTION_DETECTOR = {
        "node_name":    "/perception/pollution_detector",
        "process_name": "pollution_detector/lib/pollution_detector/pollution_detector",
    }
    RADAR_STATIC_OBSTACLES_DETECTOR = {
        "node_name":    "/perception/radar_static_obstacles_detector",
        "process_name": "radar_static_obstacles_detector/lib/radar_static_obstacles_detector/radar_static_obstacles_detector",
    }
    ROAD_LINES_3D = {
        "node_name":    "/perception/road_lines_3d",
        "process_name": "road_lines_3d/lib/road_lines_3d/road_lines_3d",
    }
    ROAD_LINES_TRACKER = {
        "node_name":    "/perception/road_lines_tracker",
        "process_name": "sat_perception_road_lines_tracker/lib/sat_perception_road_lines_tracker/road_lines_tracker_node",
    }
    ROAD_SURFACE_CONDITION_DETECTOR = {
        "node_name":    "/perception/road_surface_condition_detector",
        "process_name": "road_surface_condition_detector/lib/road_surface_condition_detector/road_surface_condition_detector",
    }
    ROADWORKS_FUSION = {
        "node_name":    "/perception/roadworks_fusion",
        "process_name": "roadworks_fusion/lib/roadworks_fusion/roadworks_fusion",
    }
    SEGMENTATION_HDMAP_FUSION = {
        "node_name":    "/perception/segmentation_hdmap_fusion",
        "process_name": "sat_perception_segmentation_hdmap_fusion/lib/sat_perception_segmentation_hdmap_fusion/segmentation_hdmap_fusion_node",
    }
    SIGNALS_CLASSIFIER = {
        "node_name":    "/perception/signals_classifier",
        "process_name": "signals_classifier/lib/signals_classifier/signals_classifier",
    }
    SPEED_LIMIT_CLASSIFIER = {
        "node_name":    "/perception/speed_limit_classifier",
        "process_name": "speed_limit_classifier/lib/speed_limit_classifier/speed_limit_classifier",
    }
    TRAFFIC_LIGHT_DETECTS = {
        "node_name":    "/perception/traffic_light_detects",
        "process_name": "__node:=traffic_light_detects",
    }
    TRAFFIC_SIGN_DETECTS = {
        "node_name":    "/perception/traffic_sign_detects",
        "process_name": "__node:=traffic_sign_detects",
    }
    TRAFFIC_SIGN_LOCALIZATION = {
        "node_name":    "/perception/traffic_sign_localization",
        "process_name": "traffic_sign_localization/lib/traffic_sign_localization/traffic_sign_localization",
    }
    VEHICLE_DETECTS = {
        "node_name":    "/perception/vehicle_detects",
        "process_name": "__node:=vehicle_detects",
    }
    LIDAR_STATIC_OBSTACLES_DETECTOR = {
        "node_name":    "/perception/lidar_static_obstacles_detector",
        "process_name": "sat_perception_lidar_static_obstacles_detector/lib/sat_perception_lidar_static_obstacles_detector/lidar_static_obstacles_detector_node",
    }
    TRAFFIC_LIGHT_PIPELINE = {
        "node_name":    "/perception/traffic_light_pipeline",
        "process_name": "sat_perception_traffic_light_pipeline/lib/sat_perception_traffic_light_pipeline/traffic_light_pipeline_node",
    }
    # Visualization nodes
    CLOUD_CLUSTERS_VISUALIZATION = {
        "node_name":    "/perception/visualization/cloud_clusters_visualization",
        "process_name": "perception_cloud_clusters_visualization/lib/perception_cloud_clusters_visualization/cloud_clusters_visualization",
    }
    PERCEPTION_LANES_VISUALIZATION_PY = {
        "node_name":    "/perception/visualization/perception_lanes_visualization_py",
        "process_name": "perception_lanes_visualization_py/lib/perception_lanes_visualization_py/perception_lanes_visualization_py",
    }
    PERCEPTION_VISUALIZATION_2D = {
        "node_name":    "/perception/visualization/perception_visualization_2d",
        "process_name": "perception_visualization_2d/lib/perception_visualization_2d/perception_visualization_2d",
    }
    OBJECTS_VISUALIZATION = {
        "node_name":    "/visualization/objects_visualization",
        "process_name": "objects_visualization/lib/objects_visualization/objects_visualization",
    }