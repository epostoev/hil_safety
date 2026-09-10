import time
import logging
import subprocess
import os


def _detect_container() -> str:
    """Автоматически определить имя контейнера стенда."""
    candidates = ["sda-f898b5d", "sda_drive"]

    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    running = result.stdout.strip().split('\n')

    for name in candidates:
        if name in running:
            return name

    raise RuntimeError(
        f"Контейнер стенда не найден. "
        f"Искали: {candidates}. "
        f"Запущены: {running}"
    )


DOCKER_CONTAINER = _detect_container()

os.environ['RMW_IMPLEMENTATION'] = 'rmw_cyclonedds_cpp'
os.environ['ROS_DOMAIN_ID'] = '1'


class BaseHILTest:
    """Базовый класс для всех HIL тестов"""
    DOCKER_CONTAINER = DOCKER_CONTAINER

    def is_alive(self) -> bool:
        """Проверить что нода присутствует в ROS graph"""
        alive = self.NODE_NAME in self.get_node_list()
        self.logger.info(f"Нода {self.NODE_NAME} жива {alive}")
        return alive

    def __init__(self, node_name: str, timeout: int = 15):
        self.node_name = node_name
        self.timeout = timeout
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(self.node_name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        # handler.setFormatter(logging.Formatter(
        #     "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        handler.setFormatter(logging.Formatter(
            "%(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"  # ← добавляет миллисекунды
        ))
        logger.addHandler(handler)
        return logger

    def run_ros(
            self,
            cmd: str,
            timeout: int = None) -> subprocess.CompletedProcess:
        """Выполнить команду в ROS 2 окружении через docker exec"""
        _timeout = timeout or self.timeout
        full_cmd = [
            "docker", "exec", self.DOCKER_CONTAINER,
            "bash", "-c",
            f"source /rep/ros2/install/setup.bash && "
            f"export ROS_DOMAIN_ID=1 && {cmd}"
        ]
        return subprocess.run(
            full_cmd, capture_output=True, text=True, timeout=_timeout
        )

    def get_node_list(self) -> list[str]:
        """Получить список активных нод из ROS graph"""
        result = self.run_ros("ros2 node list 2>/dev/null")
        result_list = []
        for n in result.stdout.split('\n'):
            if n.strip():
                result_list.append(n.strip())
        return result_list

    def setup(self):
        print(f"self = \n{type(self).__name__}\n")
        self.logger.info(f"=== Начало теста для {self.node_name} ===")

    def teardown(self):
        self.logger.info(f"=== Завершение теста для {self.node_name} ===")

    def run_ros_in_docker(
            self,
            cmd: str,
            timeout: int = None) -> subprocess.CompletedProcess:
        """
        Выполнить ROS 2 команду ВНУТРИ контейнера.
        Использует UDP транспорт вместо SHM чтобы избежать
        исчерпания SHM портов при многократных вызовах в сьюте.
        """
        _timeout = timeout or self.timeout

        # XML профиль отключает Shared Memory, оставляет только UDP.
        # Publisher (chassis_adapter_receiver) использует SHM+UDP,
        # поэтому subscriber на чистом UDP всё равно получит данные.
        xml = (
            '<?xml version="1.0" encoding="UTF-8" ?>'
            '<profiles xmlns="http://www.eprosima.com/XMLSchemas/fastRTPS_Profiles">'
            '<transport_descriptors>'
            '<transport_descriptor>'
            '<transport_id>udp</transport_id>'
            '<type>UDPv4</type>'
            '</transport_descriptor>'
            '</transport_descriptors>'
            '<participant profile_name="no_shm" is_default_profile="true">'
            '<rtps>'
            '<userTransports><transport_id>udp</transport_id></userTransports>'
            '<useBuiltinTransports>false</useBuiltinTransports>'
            '</rtps>'
            '</participant>'
            '</profiles>')

        inner = (
            f"source /rep/ros2/install/setup.bash && "
            f"export ROS_DOMAIN_ID=1 && "
            f"export FASTRTPS_DEFAULT_PROFILES_FILE=/tmp/fastdds_no_shm.xml && "
            f"{cmd}")

        full_cmd = [
            "docker", "exec", self.DOCKER_CONTAINER,
            "bash", "-c",
            f"echo '{xml}' > /tmp/fastdds_no_shm.xml && {inner}"
        ]

        return subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=_timeout
        )

    def get_topic_field(
            self,
            topic: str,
            field: str,
            timeout: int = 5) -> str | None:
        """
        Получить значение конкретного поля из топика.
        Поддерживает вложенные поля через точку.

        Примеры:
            get_topic_field("/control/system", "control_state")
            → "0"

            get_topic_field("/control/system", "imu_has_error")
            → "true"
        """
        self.logger.info(f"Читаем поле '{field}' из топика {topic}")

        result = self.run_ros_in_docker(
            f"timeout {timeout} ros2 topic echo {topic} --once 2>/dev/null",
            timeout=timeout + 3
        )

        for line in result.stdout.split('\n'):
            # Ищем строку вида "  field: value"
            stripped = line.strip()
            if stripped.startswith(f"{field}:"):
                try:
                    value = stripped.split(':', 1)[1].strip()
                    self.logger.info(f"  {field}: {value}")
                    return value
                except IndexError:
                    pass

        self.logger.warning(f"Поле '{field}' не найдено в топике {topic}")
        return None

    def get_topic_fields(
            self,
            topic: str,
            fields: list[str],
            timeout: int = 10) -> dict:
        self.logger.info(f"Читаем топик {topic}, поля: {fields}")

        result = self.run_ros_in_docker(
            f"timeout {timeout} ros2 topic echo {topic} --once 2>/dev/null",
            timeout=timeout + 5
        )
        self.logger.info(
            f"STDOUT len={len(result.stdout)}: {result.stdout[:200]}")
        self.logger.warning(f"STDERR: {result.stderr[:300]}")
        self.logger.info(f"returncode: {result.returncode}")

        if not result.stdout.strip():
            self.logger.warning(f"Пустой ответ от топика {topic}")
            return {field: None for field in fields}

        parsed = {field: None for field in fields}

        for line in result.stdout.split('\n'):
            stripped = line.strip()
            for field in fields:
                if stripped.startswith(f"{field}:"):
                    try:
                        value = stripped.split(':', 1)[1].strip()
                        parsed[field] = value
                        self.logger.info(f"  {field}: {value}")
                    except IndexError:
                        pass

        for field, value in parsed.items():
            if value is None:
                self.logger.warning(f"  {field}: не найдено")

        return parsed

    def check_control_system_errors(
        self,
        expected_errors: dict,
        monitor  # ControlSystemMonitor из фикстуры
    ) -> dict:
        self.logger.info("Проверяем флаги ошибок в /control/system")

        fields = list(expected_errors.keys()) + ["control_state", "ad_active"]
        actual = monitor.get_fields(fields)  # читаем из кэша — нет docker exec

        results = {}
        for field, expected_value in expected_errors.items():
            actual_value = actual.get(field)
            ok = actual_value == expected_value
            results[field] = {
                "expected": expected_value,
                "actual": actual_value,
                "ok": ok}
            status = "✅" if ok else "❌"
            self.logger.info(
                f"  {status} {field}: ожидалось='{expected_value}', получено='{actual_value}'"
            )

        results["control_state"] = actual.get("control_state")
        results["ad_active"] = actual.get("ad_active")
        return results

    def run_docker_command(self, cmd: str) -> subprocess.CompletedProcess:
        docker_cmd = f"docker exec {self.DOCKER_CONTAINER} {cmd}"
        self.logger.info(f"Docker exec: {cmd}")
        return subprocess.run(
            docker_cmd, shell=True, capture_output=True, text=True, timeout=10
        )

    def get_pid(self) -> int | None:
        result = self.run_docker_command(
            # f"ps aux | grep '{self.PROCESS_NAME}' | grep -v grep | grep -v python3"
            f"ps aux | grep '{self.PROCESS_NAME}'"
        )
        if result.returncode == 0 and result.stdout.strip():
            pid = int(result.stdout.strip().split('\n')[0].split()[1])
            self.logger.info(f"Найден PID: {pid}")
            return pid
        self.logger.warning("Процесс не найден")
        return None

    def kill(self) -> bool:
        self.logger.warning(f"Kill: {self.NODE_NAME}")

        pid = self.get_pid()
        if not pid:
            self.logger.error("Не удалось получить PID")
            return False

        result = self.run_docker_command(f"kill -9 {pid}")
        self.logger.info(f"kill return code: {result.returncode}")

        time.sleep(0.5)
        new_pid = self.get_pid()

        if new_pid and new_pid != pid:
            self.has_auto_restart = True
            self.logger.warning(
                f"Нода перезапущена! "
                f"Старый PID: {pid} → Новый PID: {new_pid}"
            )
        elif not new_pid:
            self.logger.info(f"Нода завершена, PID {pid} больше не существует")

        time.sleep(3)

        if self.is_alive():
            self.has_auto_restart = True
            self.logger.warning("Нода перезапущена после задержки!")
            return False

        self.logger.info("Kill успешен")
        return True

    def wait_for_death(self, timeout: int = 40, interval: int = 5) -> bool:
        self.logger.info(f"Ожидание DDS propagation, timeout={timeout}s")
        for elapsed in range(interval, timeout + 1, interval):
            time.sleep(interval)
            alive = self.is_alive()
            self.logger.info(f"[{elapsed}/{timeout}s] Нода в graph: {alive}")
            if not alive:
                self.logger.info(f"Нода исчезла после {elapsed}s")
                return True
        self.logger.error(f"Нода не исчезла за {timeout} секунд")
        return False
