class PlanningLocators:

    MANEUVER_PLANNER = {
        "node_name":    "/planning/maneuver_planner_node",
        "process_name": "maneuver_planner/lib/maneuver_planner/maneuver_planner_node",
    }
    LANE_TRACER = {
        "node_name":    "/planning/lane_tracer_node",
        "process_name": "lane_tracer/lib/lane_tracer/lane_tracer_node",
    }
    TRAJECTORY_PLANNER = {
        "node_name":    "/planning/trajectory_planner_node",
        "process_name": "trajectory_planner/lib/trajectory_planner/trajectory_planner_node",
    }
    PATH_LOADER = {
        "node_name":    "/planning/path_loader_node",
        "process_name": "path_loader/lib/path_loader/path_loader_node",
    }
    APPROXIMATE_PATHS_PUBLISHER = {
        "node_name":    "/planning/approximate_paths_publisher_node",
        "process_name": "approximate_paths_publisher/lib/approximate_paths_publisher/approximate_paths_publisher_node",
    }
    TRAJECTORY_VALIDATOR = {
        "node_name":    "/planning/trajectory_validator_node",
        "process_name": "trajectory_validator/lib/trajectory_validator/trajectory_validator_node",
    }
    PLANNING_VISUALIZATION = {
        "node_name":    "/planning/visualization/planning_visualization_node",
        "process_name": "planning_visualization/lib/planning_visualization/planning_visualization_node",
    }
    ML_PLANNER_CPP = {
        "node_name":    "/planning/ml_planner_cpp",
        "process_name": "ml_planner_cpp/lib/ml_planner_cpp/ml_planner_cpp",
    }
