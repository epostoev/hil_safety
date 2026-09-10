from framework.base_hil_test import BaseHILTest


class PredictionNode(BaseHILTest):
    NODE_NAME = "/prediction/prediction"
    PROCESS_NAME = "prediction/lib/prediction/prediction"

    def __init__(self):
        super().__init__(node_name="prediction", timeout=15)


class MlModelWrapperNode(BaseHILTest):
    NODE_NAME = "/prediction/ml_model_wrapper"  # уточнить через ros2 node list
    PROCESS_NAME = "ml_pipeline/scripts/ml_model_wrapper.py"

    def __init__(self):
        super().__init__(node_name="ml_model_wrapper", timeout=15)
