from framework.base_hil_test import BaseHILTest


class BoomBarrierDetectorNode(BaseHILTest):
    NODE_NAME = "/perception/boom_barrier_detector"
    PROCESS_NAME = "sat_perception_boom_barrier_detector/lib/sat_perception_boom_barrier_detector/boom_barrier_detector_node "

    def __init__(self):
        super().__init__(node_name="boom_barrier_detector", timeout=15)


class BoxSegmentationFusionNode(BaseHILTest):
    NODE_NAME = "/perception/box_segmentation_fusion"
    PROCESS_NAME = "sat_perception_box_segmentation_fusion/lib/sat_perception_box_segmentation_fusion/box_segmentation_fusion_node"

    def __init__(self):
        super().__init__(node_name="box_segmentation_fusion", timeout=15)


class CameraDetectsFusingNode(BaseHILTest):
    NODE_NAME = "/perception/camera_detects_fusing"
    PROCESS_NAME = "camera_detects_fusing/lib/camera_detects_fusing/camera_detects_fusing"

    def __init__(self):
        super().__init__(node_name="camera_detects_fusing", timeout=15)


class СameraMapDetectorNode(BaseHILTest):
    NODE_NAME = "/perception/camera_map_detector"
    PROCESS_NAME = "camera_map_detector/lib/camera_map_detector/camera_map_detector"

    def __init__(self):
        super().__init__(node_name="camera_map_detector", timeout=15)


class CameraTrackerCppNode(BaseHILTest):
    NODE_NAME = "/perception/camera_tracker_cpp"
    PROCESS_NAME = "camera_tracker_cpp/lib/camera_tracker_cpp/camera_tracker_cpp"

    def __init__(self):
        super().__init__(node_name="camera_tracker_cpp", timeout=15)


class СameraTracksMergerNode(BaseHILTest):
    NODE_NAME = "/perception/camera_tracks_merger"
    PROCESS_NAME = "camera_tracks_merger/lib/camera_tracks_merger/camera_tracks_merger"

    def __init__(self):
        super().__init__(node_name="camera_tracks_merger", timeout=15)


class CloudMotionDetectorNode(BaseHILTest):
    NODE_NAME = "/perception/cloud_motion_detector"
    PROCESS_NAME = "cloud_motion_detector/lib/cloud_motion_detector/cloud_motion_detector"

    def __init__(self):
        super().__init__(node_name="cloud_motion_detector", timeout=15)


class Detector3dNode(BaseHILTest):
    NODE_NAME = "/perception/detector_3d"
    PROCESS_NAME = "detector_3d/lib/detector_3d/detector_3d"

    def __init__(self):
        super().__init__(node_name="detector_3d", timeout=15)


class FrontBackboneNode(BaseHILTest):
    NODE_NAME = "/perception/front_backbone"
    PROCESS_NAME = "front_backbone/lib/front_backbone/front_backbone"

    def __init__(self):
        super().__init__(node_name="front_backbone", timeout=15)


class ImageSegmenterNode(BaseHILTest):
    NODE_NAME = "/perception/image_segmenter_cpp"
    PROCESS_NAME = "sat_perception_image_segmenter_cpp/lib/sat_perception_image_segmenter_cpp/image_segmenter_cpp_node"

    def __init__(self):
        super().__init__(node_name="image_segmenter", timeout=15)


class LidarBlindZonesNode(BaseHILTest):
    NODE_NAME = "/perception/lidar_blind_zones"
    PROCESS_NAME = "lidar_blind_zones/lib/lidar_blind_zones/lidar_blind_zones"

    def __init__(self):
        super().__init__(node_name="lidar_blind_zones", timeout=15)


class LidarNoiseDetectorNode(BaseHILTest):
    NODE_NAME = "/perception/lidar_noise_detector"
    PROCESS_NAME = "sat_perception_lidar_noise_detector/lib/sat_perception_lidar_noise_detector/lidar_noise_detector_node"

    def __init__(self):
        super().__init__(node_name="lidar_noise_detector", timeout=15)


class StaticObstaclesTrackerNode(BaseHILTest):
    NODE_NAME = "/perception/static_obstacles_tracker"
    PROCESS_NAME = "sat_perception_static_obstacles_tracker/static_obstacles_tracker_node"

    def __init__(self):
        super().__init__(node_name="static_obstacles_tracker", timeout=15)


class PointCloudClusterizerNode(BaseHILTest):
    NODE_NAME = "/perception/point_cloud_clusterizer"
    PROCESS_NAME = "point_cloud_clusterizer/lib/point_cloud_clusterizer/point_cloud_clusterizer"

    def __init__(self):
        super().__init__(node_name="point_cloud_clusterizer", timeout=15)


class PollutionDetectorNode(BaseHILTest):
    NODE_NAME = "/perception/pollution_detector_cpp"
    PROCESS_NAME = "pollution_detector_cpp/lib/sat_perception_pollution_detector_cpp/pollution_detector_cpp_node"

    def __init__(self):
        super().__init__(node_name="pollution_detector", timeout=15)


class RadarStaticObstaclesDetectorNode(BaseHILTest):
    NODE_NAME = "/perception/radar_static_obstacles_detector"
    PROCESS_NAME = "radar_static_obstacles_detector/lib/radar_static_obstacles_detector/radar_static_obstacles_detector"

    def __init__(self):
        super().__init__(node_name="radar_static_obstacles_detector", timeout=15)


class RoadLines3dNode(BaseHILTest):
    NODE_NAME = "/perception/road_lines_3d"
    PROCESS_NAME = "road_lines_3d/lib/road_lines_3d/road_lines_3d"

    def __init__(self):
        super().__init__(node_name="road_lines_3d", timeout=15)


class RoadLinesTrackerNode(BaseHILTest):
    NODE_NAME = "/perception/road_lines_tracker"
    PROCESS_NAME = "sat_perception_road_lines_tracker/lib/sat_perception_road_lines_tracker/road_lines_tracker_node"

    def __init__(self):
        super().__init__(node_name="road_lines_tracker", timeout=15)


class RoadSurfaceConditionDetectorNode(BaseHILTest):
    NODE_NAME = "/perception/road_surface_condition_detector_cpp"
    PROCESS_NAME = "sat_perception_road_surface_condition_detector_cpp/lib/sat_perception_road_surface_condition_detector_cpp/road_surface_condition_detector_cpp_node"

    def __init__(self):
        super().__init__(node_name="road_surface_condition_detector", timeout=15)


class RoadworksFusionNode(BaseHILTest):
    NODE_NAME = "/perception/roadworks_fusion"
    PROCESS_NAME = "roadworks_fusion/lib/roadworks_fusion/roadworks_fusion"

    def __init__(self):
        super().__init__(node_name="roadworks_fusion", timeout=15)


class SegmentationHdmapFusionNode(BaseHILTest):
    NODE_NAME = "/perception/segmentation_hdmap_fusion"
    PROCESS_NAME = "sat_perception_segmentation_hdmap_fusion/lib/sat_perception_segmentation_hdmap_fusion/segmentation_hdmap_fusion_node"

    def __init__(self):
        super().__init__(node_name="segmentation_hdmap_fusion", timeout=15)


class SignalsСlassifierNode(BaseHILTest):
    NODE_NAME = "/perception/signals_classifier_cpp"
    PROCESS_NAME = "sat_perception_signals_classifier_cpp/lib/sat_perception_signals_classifier_cpp/signals_classifier_cpp_node"

    def __init__(self):
        super().__init__(node_name="signals_classifier", timeout=15)


class SpeedLimitClassifierNode(BaseHILTest):
    NODE_NAME = "/perception/speed_limit_classifier"
    PROCESS_NAME = "speed_limit_classifier/lib/speed_limit_classifier/speed_limit_classifier"

    def __init__(self):
        super().__init__(node_name="speed_limit_classifier", timeout=15)


class TrafficLightDetectsNode(BaseHILTest):
    NODE_NAME = "/perception/traffic_light_detects"
    PROCESS_NAME = "__node:=traffic_light_detects"

    def __init__(self):
        super().__init__(node_name="traffic_light_detects", timeout=15)


class TrafficSignDetectsNode(BaseHILTest):
    NODE_NAME = "/perception/traffic_sign_detects"
    PROCESS_NAME = "__node:=traffic_sign_detects"

    def __init__(self):
        super().__init__(node_name="traffic_sign_detects", timeout=15)


class TrafficSignLocalizationNode(BaseHILTest):
    NODE_NAME = "/perception/traffic_sign_localization"
    PROCESS_NAME = "traffic_sign_localization/lib/traffic_sign_localization/traffic_sign_localization"

    def __init__(self):
        super().__init__(node_name="traffic_sign_localization", timeout=15)


class VehicleDetectsNode(BaseHILTest):
    NODE_NAME = "/perception/vehicle_detects"
    PROCESS_NAME = "__node:=vehicle_detects"

    def __init__(self):
        super().__init__(node_name="vehicle_detects", timeout=15)


class LidarStaticObstaclesDetectorNode(BaseHILTest):
    NODE_NAME = "/perception/lidar_static_obstacles_detector"
    PROCESS_NAME = "sat_perception_lidar_static_obstacles_detector/lib/sat_perception_lidar_static_obstacles_detector/lidar_static_obstacles_detector_nod"

    def __init__(self):
        super().__init__(node_name="lidar_static_obstacles_detector", timeout=15)


class CloudClustersVisualizationNode(BaseHILTest):
    NODE_NAME = "/perception/visualization/cloud_clusters_visualization"
    PROCESS_NAME = "perception_cloud_clusters_visualization/lib/perception_cloud_clusters_visualization/cloud_clusters_visualization"

    def __init__(self):
        super().__init__(node_name="cloud_clusters_visualization", timeout=15)


class PerceptionLanesVisualizationPyNode(BaseHILTest):
    NODE_NAME = "/perception/visualization/perception_lanes_visualization_py"
    PROCESS_NAME = "perception_lanes_visualization_py/lib/perception_lanes_visualization_py/perception_lanes_visualization_py"

    def __init__(self):
        super().__init__(node_name="perception_lanes_visualization_py", timeout=15)


class PerceptionVisualization2dNode(BaseHILTest):
    NODE_NAME = "/perception/visualization/perception_visualization_2d"
    PROCESS_NAME = "/perception_visualization_2d/lib/perception_visualization_2d/perception_visualization_2d"

    def __init__(self):
        super().__init__(node_name="perception_visualization_2d", timeout=15)


class TrafficLightPipelineNode(BaseHILTest):
    NODE_NAME = "/perception/traffic_light_pipeline"
    PROCESS_NAME = "sat_perception_traffic_light_pipeline/lib/sat_perception_traffic_light_pipeline/traffic_light_pipeline_node"

    def __init__(self):
        super().__init__(node_name="traffic_light_pipeline", timeout=15)


class ObjectsVisualizationNode(BaseHILTest):
    NODE_NAME = "/visualization/objects_visualization"
    PROCESS_NAME = "sobjects_visualization/lib/objects_visualization/objects_visualization"

    def __init__(self):
        super().__init__(node_name="objects_visualization", timeout=15)
