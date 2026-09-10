# HIL Test Framework

Автоматизированный тестовый фреймворк для HIL-стенда.
Тестирование нод ROS 2 автономного транспортного средства.

## Структура проекта

tests/
├── conftest.py
├── framework/
│   ├── base_hil_test.py        # Базовый класс
│   ├── carapi_node.py          # Управление /carapi_node
│   └── trajectory_planner_node.py  # Управление /planning/trajectory_planner_node
└── fault_injection/
    ├── test_carapi_kill.py
    └── test_trajectory_planner_kill.py

## Запуск тестов

# Все тесты
pytest tests/ -v -s --log-cli-level=INFO

# Только fault injection
pytest tests/fault_injection/ -v -s --log-cli-level=INFO

# C HTML-report
pytest tests/fault_injection/ -v -s --log-cli-level=INFO

## Требования

- Python 3.10+
- ROS 2 Humble
- Docker (контейнер sda-f898b5d)
- pytest, pytest-timeout, pytest-rerunfailures
```

---

## Итоговая картина проекта
```
tests/
├── conftest.py                          ✅
├── framework/
│   ├── base_hil_test.py                 ✅
│   ├── carapi_node.py                   ✅
│   └── trajectory_planner_node.py       ✅ (с последним фиксом)
└── fault_injection/
    ├── test_carapi_kill.py              ✅
    └── test_trajectory_planner_kill.py  ✅


# HIL Test Framework — План развития на 6 недель

## Неделя 1 — HTML отчёты и документация
- [ ] Добавить колонки `Ожидаемый результат` / `Фактический результат` во все тесты
- [ ] Добавить `make report-sensing-kill` для отчёта по fault injection тестам
- [ ] Обновить `README.md` и Confluence — актуальная структура проекта
- [ ] Убрать отладочные `print()` и `input()` из кода

## Неделя 2 — Рефакторинг фреймворка
- [ ] Перевести все старые ноды (`imu_node.py`, `trajectory_planner_node.py` и др.) на общие методы из `BaseHILTest` — убрать дублирование кода
- [ ] Вынести константы (`DOCKER_CONTAINER`, пути к `setup.bash`) в единый `config.py`
- [ ] Добавить `has_auto_restart = False` в `BaseHILTest.__init__` чтобы не повторять в каждом классе

## Неделя 3 — Расширение покрытия нод
- [ ] Написать тесты для оставшихся нод: `/teleops/manager`, `/teleops/webrtc_primary`, `/visualization/rviz_world_node`
- [ ] Добавить `test_sensing_nodes_running` для всех новых нод

## Неделя 4 — MRM мониторинг для всех нод
- [ ] Добавить `expected`/`actual` в `test_sensing_kill.py` для HTML отчёта
- [ ] Запустить `test_sensing_kill.py` на всех нодах и зафиксировать baseline значения MRM топика
- [ ] Добавить `make report-sensing-kill` в Makefile

## Неделя 5 — Стабильность и надёжность
- [ ] Добавить автоочистку SHM перед каждым запуском тестов в Makefile
- [ ] Настроить `pytest-rerunfailures` для нестабильных тестов
- [ ] Настроить логирование в файл через `pytest.ini`
- [ ] Добавить проверку что стенд готов перед запуском тестов

## Неделя 6 — CI/CD и итоги
- [ ] Настроить автозапуск тестов по расписанию или по триггеру
- [ ] Добавить отправку HTML отчёта в Confluence автоматически
- [ ] Финальный прогон всех тестов на двух стендах (`sda-f898b5d` и `sda_drive`)
- [ ] Итоговая документация в Confluence



## Полезные команды

`ros2 topic echo --full-length safety/mrm_request | grep -A 5 "error_code: 131346"`

`pytest -v -s tests/fault_injection/test_planning_kill.py`