import pytest

PERCEPTION_NODES = [
        ("perception_boom_barrier_detector_node",                               "TC-PER-PRE-001", "/perception/boom_barrier_detector"),
        ("perception_box_segmentation_fusion_node",                             "TC-PER-PRE-002", "/perception/box_segmentation_fusion"),
        # ("perception_camera_detects_fusing_node",                               "TC-PER-PRE-003", "/perception/camera_detects_fusing"),
        ("perception_camera_map_detector_node",                                 "TC-PER-PRE-004", "/perception/camera_map_detector"),
        ("perception_camera_tracker_cpp_node",                                  "TC-PER-PRE-005", "/perception/camera_tracker_cpp"),
        ("perception_camera_tracks_merger_node",                                "TC-PER-PRE-006", "/perception/camera_tracks_merger"),
        ("perception_cloud_motion_detector_node",                               "TC-PER-PRE-007", "/perception/cloud_motion_detector"),
        ("perception_detector_3d_node",                                         "TC-PER-PRE-008", "/perception/detector_3d"),
        # ("perception_front_backbone_node",                                      "TC-PER-PRE-009", "/perception/front_backbone"),
        ("perception_image_segmenter_cpp_node",                                 "TC-PER-PRE-010", "/perception/image_segmenter_cpp"),
        ("perception_lidar_blind_zones_node",                                   "TC-PER-PRE-011", "/perception/lidar_blind_zones"),
        ("perception_lidar_noise_detector_node",                                "TC-PER-PRE-012", "/perception/lidar_noise_detector"),
        # ("perception_static_obstacles_tracker_node",                            "TC-PER-PRE-013", "/perception/static_obstacles_tracker"),
        ("perception_point_cloud_clusterizer_node",                             "TC-PER-PRE-014", "/perception/point_cloud_clusterizer"),
        ("perception_pollution_detector_node",                                  "TC-PER-PRE-015", "/perception/pollution_detector_cpp"),
        ("perception_radar_static_obstacles_detector_node",                     "TC-PER-PRE-016", "/perception/radar_static_obstacles_detector"),
        ("perception_road_lines_3d_node",                                       "TC-PER-PRE-017", "/perception/road_lines_3d"),
        ("perception_road_lines_tracker_node",                                  "TC-PER-PRE-018", "/perception/road_lines_tracker"),
        ("perception_road_surface_condition_detector_node",                     "TC-PER-PRE-019", "/perception/road_surface_condition_detector_cpp"),
        ("perception_roadworks_fusion_node",                                    "TC-PER-PRE-020", "/perception/roadworks_fusion"),
        # ("perception_segmentation_hdmap_fusion_node",                           "TC-PER-PRE-021", "/perception/segmentation_hdmap_fusion_node"),
        ("perception_signals_classifier_node",                                  "TC-PER-PRE-022", "/perception/signals_classifier_cpp"),
        ("perception_speed_limit_classifier_node",                              "TC-PER-PRE-023", "/perception/speed_limit_classifier"),
        # ("perception_traffic_light_detects_node",                               "TC-PER-PRE-024", "/perception/traffic_light_detects"),
        # ("perception_traffic_sign_detects_node",                                "TC-PER-PRE-025", "/perception/traffic_sign_detects"),
        ("perception_traffic_sign_localization_node",                           "TC-PER-PRE-026", "/perception/traffic_sign_localization"),
        # ("perception_vehicle_detects_node",                                     "TC-PER-PRE-027", "/perception/vehicle_detects"),
        ("perception_lidar_static_obstacles_detector_node",                     "TC-PER-PRE-028", "/perception/lidar_static_obstacles_detector"),
        ("perception_visualization_cloud_clusters_visualization_node",          "TC-PER-PRE-029", "/perception/visualization/cloud_clusters_visualization"),
        ("perception_visualization_perception_lanes_visualization_py_node",     "TC-PER-PRE-030", "/perception/visualization/perception_lanes_visualization_py"),
        ("perception_visualization_perception_visualization_2d_node",           "TC-PER-PRE-031", "/perception/visualization/perception_visualization_2d"),
        # ("perception_traffic_light_pipeline_node",                              "TC-PER-PRE-032", "/perception/traffic_light_pipeline"),
        ("perception_visualization_objects_visualization_node",                 "TC-PER-PRE-033", "/visualization/objects_visualization")
]

class TestPerceptionNodesRunning:
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", PERCEPTION_NODES)
    def test_node_running(self, fixture_name, tc_id, node_name, request):
        f"""{tc_id}: {node_name} присутствует в ROS graph"""

        node = request.getfixturevalue(fixture_name)

        request.node.expected = f"Нода {node_name} присутствует в ROS graph"

        if not node.is_alive():
            request.node.actual = "Нода не запущена — SKIPPED"
            pytest.skip(f"Нода {node_name} не запущена")

        assert node.is_alive() is True

        request.node.actual = f"Нода {node_name} жива ✅"