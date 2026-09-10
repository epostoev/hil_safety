FROM artifactory.sberautotech.ru:5574/infra/sat-base-images/sat-ubuntu:22.04-amd64-20240513

ENV DEBIAN_FRONTEND=noninteractive

# Базовые инструменты (без docker.io)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common \
    python3-pip \
    iputils-ping \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Docker CLI — через внутреннее зеркало artifactory (download.docker.com
# недоступен с этой сети). Паттерн взят из SDA-dev scripts/adu/Dockerfile
# (там подтверждённо рабочий на этой же сети). Версия не пинится явно —
# неизвестно, есть ли в sat-docker-mirror-local конкретно 24.0.7; исходный
# автор dockerfile указывал её ради совместимости с API хоста (1.43) —
# если после сборки docker exec с хоста начнёт вести себя странно, стоит
# явно проверить версию docker-ce-cli внутри контейнера и при
# необходимости уточнить у инфраструктурной команды доступные версии.
RUN echo "deb [arch=$(dpkg --print-architecture)] https://artifactory.sberautotech.ru/artifactory/sat-docker-mirror-local jammy stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# ROS2 Humble — через внутреннее зеркало artifactory (raw.githubusercontent.com
# и packages.ros.org недоступны с этой сети). Паттерн и адрес зеркала взяты
# из SDA-dev docker/Dockerfile:165 (sat-ubuntu-3rdparty-local, компонент
# "ros"), там подтверждённо рабочий.
#
# ros-humble-ros-base и python3-colcon-common-extensions в этом зеркале НЕ
# публикуются (проверено на реальной сборке 2026-08-19: "Unable to locate
# package" для обоих, остальные 4 пакета ниже нашлись нормально).
# ros-humble-ros-base убран из списка: локальный ROS2 внутри этого образа
# фактически не используется программно -- весь код проекта (base_hil_test.py
# run_ros(), mrm_request_monitor.py start()) выполняет `ros2 ...` через
# `docker exec <SDA_CONTAINER> ...` внутри контейнера СТЕНДА, у которого уже
# есть полноценный ROS2 (/rep/ros2/install/). Локальный ros2cli и компания
# здесь нужны разве что для ручного `make debug`. Если после сборки что-то
# из перечисленных CLI-пакетов не заработает из-за недостающих транзитивных
# зависимостей ros-humble-ros-base -- тогда возвращаемся к вопросу отдельно.
# python3-colcon-common-extensions перенесён в pip3 install ниже (пакет
# называется там colcon-common-extensions, не python3-colcon-common-extensions).
RUN echo "deb https://artifactory.sberautotech.ru/artifactory/sat-ubuntu-3rdparty-local jammy ros" \
    > /etc/apt/sources.list.d/ros2.list

RUN apt-get update && apt-get install -y \
    ros-humble-ros2cli \
    ros-humble-ros2topic \
    ros-humble-ros2node \
    ros-humble-ros2service \
    && rm -rf /var/lib/apt/lists/*

# Python зависимости
RUN pip3 install \
    pytest \
    pytest-timeout \
    pytest-rerunfailures \
    pytest-html \
    allure-pytest \
    pyyaml \
    psutil \
    requests \
    colcon-common-extensions \
    --index-url https://artifactory.sberautotech.ru/artifactory/api/pypi/pypi/simple/ \
    --trusted-host artifactory.sberautotech.ru

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

COPY tests/ /workspace/tests/

WORKDIR /workspace

CMD ["pytest", "tests/fault_injection/", "-v", "-s"]