import pytest
import allure

from framework.kill_fault_injection import run_kill_fault_injection


PREDICTION_NODES = [
    ("prediction_node_alive",             "TC-PRD-KILL-001", "/prediction"),
    # ("prediction_ml_model_wrapper_alive", "TC-PRD-KILL-002", "/prediction/ml_model_wrapper"),
]


@allure.epic("HIL Testing")
@allure.feature("Prediction")
@allure.story("Fault Injection: kill -6 нод")
@allure.title("Fault Injection: принудительное завершение нод компонента Prediction")
@allure.description(
    "Тест отправляет kill -6 каждой ноде компонента Prediction "
    "и проверяет что MRM реагирует переходом mrm_type: 0 → 2 "
    "в течение 5000ms."
)
class TestPredictionKill:
    """
    Fault Injection: принудительное завершение нод компонента Prediction.

    TC-PRD-KILL-001: /prediction/prediction
    TC-PRD-KILL-002: /prediction/ml_model_wrapper
    """

    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("fixture_name, tc_id, node_name", PREDICTION_NODES)
    def test_prediction_kill(self, fixture_name, tc_id, node_name,
                             mrm_monitor, request, restart_autopilot_after):

        allure.dynamic.title(f"{tc_id}: kill -6 {node_name}")
        allure.dynamic.parameter("node_name", node_name)
        allure.dynamic.parameter("tc_id", tc_id)

        with allure.step(f"Получить объект ноды {node_name}"):
            node = request.getfixturevalue(fixture_name)

        run_kill_fault_injection(node, node_name, mrm_monitor, request, sla_ms=5000)