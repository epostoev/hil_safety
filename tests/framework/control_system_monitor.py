import subprocess
import threading
from framework.base_hil_test import DOCKER_CONTAINER


class ControlSystemMonitor:
    """
    Читает /control/system непрерывно в фоновом треде.
    Один docker exec на весь сьют — нет SHM исчерпания.
    Паттерн взят из TopicWatcher коллеги.
    """
    CONTAINER = DOCKER_CONTAINER

    def __init__(self):
        self._latest_raw: str = ""
        self._lock = threading.Lock()
        self._proc = None
        self._thread = None
        self._running = False
        self._first_message = threading.Event()

    def start(self):
        cmd = [
            "docker", "exec", self.CONTAINER,
            "bash", "-c",
            "source /rep/ros2/install/setup.bash && "
            "export ROS_DOMAIN_ID=1 && "
            "ros2 topic echo /control/system"  # убрали 2>/dev/null
        ]
        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # было DEVNULL
            text=True,
            bufsize=1
        )
        # Читаем stderr в отдельном треде для диагностики

        def log_stderr():
            for line in self._proc.stderr:
                print(f"[MONITOR STDERR] {line.rstrip()}", flush=True)
        threading.Thread(target=log_stderr, daemon=True).start()

        self._running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def _read_loop(self):
        buffer = []
        for line in self._proc.stdout:
            if not self._running:
                break
            if line.strip() == "---":
                raw = "\n".join(buffer)
                buffer = []
                if raw.strip():
                    with self._lock:
                        self._latest_raw = raw
                    self._first_message.set()
            else:
                buffer.append(line.rstrip())

    def wait_ready(self, timeout: int = 15) -> bool:
        """Ждём первого сообщения перед началом тестов"""
        return self._first_message.wait(timeout=timeout)

    def get_field(self, field: str) -> str | None:
        """Получить значение поля из последнего сообщения"""
        with self._lock:
            raw = self._latest_raw
        for line in raw.split("\n"):
            stripped = line.strip()
            if stripped.startswith(f"{field}:"):
                try:
                    return stripped.split(":", 1)[1].strip()
                except IndexError:
                    return None
        return None

    def get_fields(self, fields: list[str]) -> dict:
        """Получить несколько полей из последнего сообщения"""
        with self._lock:
            raw = self._latest_raw
        result = {f: None for f in fields}
        for line in raw.split("\n"):
            stripped = line.strip()
            for field in fields:
                if stripped.startswith(f"{field}:"):
                    try:
                        result[field] = stripped.split(":", 1)[1].strip()
                    except IndexError:
                        pass
        return result

    def stop(self):
        self._running = False
        if self._proc:
            self._proc.kill()
            self._proc.communicate()
