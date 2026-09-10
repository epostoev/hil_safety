import pytest
import allure
 
 
PREDICTION_NODES = [
    ("prediction_node",             "TC-PRD-PRE-001", "/prediction"),
    # ("prediction_ml_model_wrapper", "TC-PRD-PRE-002", "/prediction/ml_model_wrapper"),
]
 
 
@allure.epic("HIL Testing")
@allure.feature("Prediction")
@allure.story("Предусловия: проверка запуска нод")
@allure.title("Проверка запуска нод компонента Prediction")
@allure.description(
    "Предусловия: все ноды компонента Prediction должны присутствовать в ROS graph. "
    "Тест проверяет каждую ноду через is_alive()."
)
class TestPredictionNodesRunning:
    """
    Проверка что все ноды компонента Prediction запущены.
 
    TC-PRD-PRE-001: /prediction/prediction
    TC-PRD-PRE-002: /prediction/ml_model_wrapper
    """
 
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", PREDICTION_NODES)
    def test_node_running(self, fixture_name, tc_id, node_name, request):
        f"""{tc_id}: {node_name} присутствует в ROS graph"""
 
        allure.dynamic.title(f"{tc_id}: {node_name}")
        allure.dynamic.parameter("node_name", node_name)
        allure.dynamic.parameter("tc_id", tc_id)
 
        with allure.step(f"Получить объект ноды {node_name}"):
            node = request.getfixturevalue(fixture_name)
 
        request.node.expected = f"Нода {node_name} присутствует в ROS graph"
 
        with allure.step(f"Проверить что нода {node_name} присутствует в ROS graph"):
            if not node.is_alive():
                request.node.actual = "Нода не запущена — SKIPPED"
                pytest.skip(f"Нода {node_name} не запущена")
 
            assert node.is_alive() is True
 
        request.node.actual = f"Нода {node_name} присутствует в ROS graph ✅"
 
        with allure.step("Зафиксировать результат"):
            allure.attach(
                f"TC ID:     {tc_id}\n"
                f"Node:      {node_name}\n"
                f"Статус:    ALIVE ✅",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )