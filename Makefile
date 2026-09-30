IMAGE = my-docker-project_v_2
TAG = latest

PROJECT_DIR ?= $(shell pwd)
SDA_CONTAINER := $(shell docker ps --format '{{.Names}}' | grep -E 'sda-f898b5d|sda_drive' | head -1)

# Проверка что контейнер найден
ifeq ($(SDA_CONTAINER),)
$(error Контейнер стенда не найден. Запусти: docker ps)
endif

# Allure TestOps
# ALLURE_SERVER  = https://allure-testops.sberautotech.ru
ALLURE_SERVER  = https://testops.navio.auto/
HIL_PROJECT_ID = 24

# Общие флаги docker run
DOCKER_RUN = docker run --rm \
	--name evgeny_tests \
	--network host \
	--pid=container:$(SDA_CONTAINER) \
	-e SDA_CONTAINER=$(SDA_CONTAINER) \
	-v /var/run/docker.sock:/var/run/docker.sock

DOCKER_RUN_ALLURE = $(DOCKER_RUN) \
	-v $(PROJECT_DIR)/allure-results:/workspace/allure-results \
	-v $(PROJECT_DIR)/tests:/workspace/tests

# =============================================================================
# Базовые команды
# =============================================================================

# build:
# 	docker build -f $(PROJECT_DIR)/dockerfile -t $(IMAGE):$(TAG) $(PROJECT_DIR)
build:
	docker build --network host -f $(PROJECT_DIR)/dockerfile -t $(IMAGE):$(TAG) $(PROJECT_DIR)

# docker build -f $(PROJECT_DIR)/dockerfile -t $(IMAGE):$(TAG) $(PROJECT_DIR)
# docker build --no-cache -f $(PROJECT_DIR)/dockerfile -t $(IMAGE):$(TAG) $(PROJECT_DIR)
# docker build --pull=false --no-cache -f $(PROJECT_DIR)/dockerfile -t $(IMAGE):$(TAG) $(PROJECT_DIR)
# rebuild:
# 	docker build --pull=false --no-cache -f /home/sda/repos/sda/HIL/dockerfile -t my-docker-project_v_2:latest /home/sda/repos/sda/HIL

rebuild:
	docker build --network host --no-cache -f $(PROJECT_DIR)/dockerfile -t $(IMAGE):$(TAG) $(PROJECT_DIR)


run:
	$(DOCKER_RUN) $(IMAGE):$(TAG)

run-sensing:
	$(DOCKER_RUN) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_sensing_nodes_running.py -v -s

test:
	$(DOCKER_RUN) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/$(FILE) -v -s

dev:
	docker run -it --rm \
		--name evgeny_dev \
		--network host \
		--pid=container:$(SDA_CONTAINER) \
		-e SDA_CONTAINER=$(SDA_CONTAINER) \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PROJECT_DIR)/tests:/workspace/tests \
		$(IMAGE):$(TAG)

debug:
	docker run -it --rm \
		--name evgeny_debug \
		--network host \
		--pid=container:$(SDA_CONTAINER) \
		-e SDA_CONTAINER=$(SDA_CONTAINER) \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PROJECT_DIR)/tests:/workspace/tests \
		--entrypoint bash \
		$(IMAGE):$(TAG)

stop:
	docker stop evgeny_tests || true

clean:
	docker rm -f evgeny_tests || true
	docker rmi $(IMAGE):$(TAG) || true

# =============================================================================
# Запуск тестов по компонентам (сбор allure-results)
# =============================================================================

allure_sensing:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_sensing_nodes_running.py \
		       tests/fault_injection/test_sensing_kill.py \
		-v -s --alluredir=allure-results/sensing

allure_perception:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_perception_nodes_running.py \
		       tests/fault_injection/test_perception_kill.py \
		-v -s --alluredir=allure-results/perception

allure_planning:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_planning_nodes_running.py \
		       tests/fault_injection/test_planning_kill.py \
		-v -s --alluredir=allure-results/planning

allure_localization:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_localization_nodes_running.py \
		       tests/fault_injection/test_localization_kill.py \
		-v -s --alluredir=allure-results/localization

allure_calibration:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_calibration_nodes_running.py \
		        tests/fault_injection/test_calibration_kill.py \
		-v -s --alluredir=allure-results/calibration 

allure_control:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_control_nodes_running.py \
		       tests/fault_injection/test_control_kill.py \
		-v -s --alluredir=allure-results/control

allure_hdmap:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_hdmap_nodes_running.py \
		       tests/fault_injection/test_hdmap_kill.py \
		-v -s --alluredir=allure-results/hdmap

allure_prediction:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_prediction_nodes_running.py \
		       tests/fault_injection/test_prediction_kill.py \
		-v -s --alluredir=allure-results/prediction

allure_integration:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/test_integration_nodes_running.py \
		       tests/fault_injection/test_integration_kill.py \
		-v -s --alluredir=allure-results/integration

allure_lidar:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/sensing/test_lidars.py \
		-v -s --alluredir=allure-results/lidars

allure_radar:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/sensing/test_radars.py \
		-v -s --alluredir=allure-results/radars

allure_imu:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/sensing/test_imu.py \
		-v -s --alluredir=allure-results/imu

allure_camera:
	$(DOCKER_RUN_ALLURE) $(IMAGE):$(TAG) \
		pytest tests/fault_injection/sensing/test_cameras.py \
		-v -s --alluredir=allure-results/cameras

# =============================================================================
# Загрузка результатов на Allure TestOps через allurectl
# Требует: ALLURE_TESTOPS_TOKEN в ~/.bashrc
# Утилита: ~/allurectl (установить один раз)
# =============================================================================

allure-upload-sensing:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Sensing Kill Tests" \
	~/allurectl upload allure-results/sensing

allure-upload-perception:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Perception Kill Tests" \
	~/allurectl upload allure-results/perception

allure-upload-planning:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Planning Kill Tests" \
	~/allurectl upload allure-results/planning

allure-upload-localization:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Localization Kill Tests" \
	~/allurectl upload allure-results/localization

allure-upload-calibration:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Calibration Kill Tests" \
	~/allurectl upload allure-results/calibration

allure-upload-control:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Control Kill Tests" \
	~/allurectl upload allure-results/control

allure-upload-hdmap:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="HDMap Kill Tests" \
	~/allurectl upload allure-results/hdmap

allure-upload-prediction:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Prediction Kill Tests" \
	~/allurectl upload allure-results/prediction

allure-upload-integration:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Integration Kill Tests" \
	~/allurectl upload allure-results/integration

allure-upload-lidar:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Lidar power off" \
	~/allurectl upload allure-results/lidars

allure-upload-radar:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Radar power off" \
	~/allurectl upload allure-results/radars

allure-upload-imu:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Imu power off" \
	~/allurectl upload allure-results/imu

allure-upload-camera:
	ALLURE_ENDPOINT=$(ALLURE_SERVER) \
	ALLURE_TOKEN=$(ALLURE_TESTOPS_TOKEN) \
	ALLURE_PROJECT_ID=$(HIL_PROJECT_ID) \
	ALLURE_LAUNCH_NAME="Camera broke config" \
	~/allurectl upload allure-results/cameras

# =============================================================================
# run-all — запустить ВСЕ тесты последовательно и загрузить на сервер
# Использование: make run-all
# =============================================================================

run-all:
	@echo "======================================================"
	@echo " HIL Fault Injection — запуск всех компонентов"
	@echo " Сервер: $(ALLURE_SERVER)"
	@echo " Проект: $(HIL_PROJECT_ID)"
	@echo "======================================================"

	@echo "\n>>> [1/10] Sensing"
	-$(MAKE) allure_sensing
	-$(MAKE) allure-upload-sensing

	@echo "\n>>> [2/10] Perception"
	-$(MAKE) allure_perception
	-$(MAKE) allure-upload-perception

	@echo "\n>>> [3/10] Planning"
	-$(MAKE) allure_planning
	-$(MAKE) allure-upload-planning

	@echo "\n>>> [4/10] Localization"
	-$(MAKE) allure_localization
	-$(MAKE) allure-upload-localization

	@echo "\n>>> [5/10] Calibration"
	-$(MAKE) allure_calibration
	-$(MAKE) allure-upload-calibration

	@echo "\n>>> [6/10] Control"
	-$(MAKE) allure_control
	-$(MAKE) allure-upload-control

	@echo "\n>>> [7/10] HD-Map"
	-$(MAKE) allure_hdmap
	-$(MAKE) allure-upload-hdmap

	@echo "\n>>> [8/10] Prediction"
	-$(MAKE) allure_prediction
	-$(MAKE) allure-upload-prediction

	@echo "\n>>> [9/10] Integration"
	-$(MAKE) allure_integration
	-$(MAKE) allure-upload-integration

	@echo "\n>>> [10/10] Integration"
	-$(MAKE) allure_integration
	-$(MAKE) allure-upload-integration

	@echo "\n======================================================"
	@echo " Готово! Результаты доступны на:"
	@echo " $(ALLURE_SERVER)/project/$(HIL_PROJECT_ID)/launches"
	@echo "======================================================"

.PHONY: build rebuild run run-sensing test dev debug stop clean \
        allure_sensing allure_perception allure_planning allure_localization \
        allure_calibration allure_control allure_hdmap allure_prediction allure_integration \
        allure-upload-sensing allure-upload-perception allure-upload-planning \
        allure-upload-localization allure-upload-calibration allure-upload-control \
        allure-upload-hdmap allure-upload-prediction allure-upload-integration \
        run-all