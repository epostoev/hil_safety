import json
import subprocess
import threading
import time


class MrmRequestMonitor:
    """
    Читает /safety/mrm_request непрерывно в фоновом треде.
    Один docker exec на весь сьют — нет SHM исчерпания.
    """

    def __init__(self, container: str):
        self.container = container
        self._latest_raw: str = ""
        self._latest_stamp: str = ""  # ← sec.nanosec
        self._lock = threading.Lock()
        self._proc = None
        self._thread = None
        self._running = False
        self._first_message = threading.Event()

    def start(self):
        cmd = [
            "docker", "exec", self.container,
            "bash", "-c",
            "source /rep/ros2/install/setup.bash && "
            "export ROS_DOMAIN_ID=1 && "
            "ros2 topic echo --full-length /safety/mrm_request 2>/dev/null"
        ]
        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1
        )
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
                        # Парсим stamp из сообщения
                        sec = nanosec = None
                        for l in raw.split("\n"):
                            s = l.strip()
                            if s.startswith("sec:"):
                                sec = s.split(":")[1].strip()
                            elif s.startswith("nanosec:"):
                                nanosec = s.split(":")[1].strip()
                        if sec and nanosec:
                            self._latest_stamp = f"{sec}.{nanosec}"
                    self._first_message.set()
            else:
                buffer.append(line.rstrip())

    def wait_ready(self, timeout: int = 15) -> bool:
        return self._first_message.wait(timeout=timeout)

    def get_fields(self, fields: list[str]) -> dict:
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

    def get_stamp(self) -> str:
        """Получить текущий timestamp последнего сообщения."""
        with self._lock:
            return self._latest_stamp

    def wait_for_mrm_type_change(
        self,
        from_value: str,
        to_value: str,
        before_stamp: str = None,   # ← добавить параметр
        timeout: float = 10.0,
        poll_interval: float = 0.01
    ) -> dict:
        # Используем переданный stamp или берём текущий
        if before_stamp is None:
            with self._lock:
                before_stamp = self._latest_stamp

        before_sec, before_ns = self._parse_stamp(before_stamp)
        start = time.time()

        while time.time() - start < timeout:
            with self._lock:
                current_stamp = self._latest_stamp
                raw = self._latest_raw

            if current_stamp != before_stamp:
                current_mrm = None
                for line in raw.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("mrm_type:"):
                        current_mrm = stripped.split(":")[1].strip()
                        break

                if current_mrm == to_value:
                    after_sec, after_ns = self._parse_stamp(current_stamp)
                    reaction_ns = (after_sec - before_sec) * 1_000_000_000 + \
                        (after_ns - before_ns)
                    reaction_ms = round(reaction_ns / 1_000_000, 3)

                    return {
                        "success": True,
                        "reaction_ms": reaction_ms,
                        "reaction_ns": reaction_ns,
                        "mrm_type": current_mrm,
                        "stamp_before": before_stamp,
                        "stamp_after": current_stamp,
                    }

                before_stamp = current_stamp
                before_sec, before_ns = self._parse_stamp(current_stamp)

            time.sleep(poll_interval)

        return {
            "success": False,
            "reaction_ms": None,
            "reaction_ns": None,
            "mrm_type": self.get_fields(["mrm_type"]).get("mrm_type"),
            "stamp_before": before_stamp,
            "stamp_after": None,
        }

    def wait_for_error_code(
        self,
        error_code: int,
        before_stamp: str = None,
        timeout: float = 10.0,
        poll_interval: float = 0.01
    ) -> dict:
        """
        Ждёт появления заданного error_code в error_codes сообщения
        /safety/mrm_request (в отличие от wait_for_mrm_type_change,
        не привязан к смене mrm_type — некоторые отказы могут не
        эскалировать mrm_type, но добавлять запись в error_codes).
        """
        if before_stamp is None:
            with self._lock:
                before_stamp = self._latest_stamp

        before_sec, before_ns = self._parse_stamp(before_stamp)
        start = time.time()

        while time.time() - start < timeout:
            with self._lock:
                current_stamp = self._latest_stamp

            if current_stamp != before_stamp:
                match = next(
                    (c for c in self.get_error_codes()
                     if c["error_code"] == error_code),
                    None
                )
                if match is not None:
                    after_sec, after_ns = self._parse_stamp(current_stamp)
                    reaction_ns = (after_sec - before_sec) * 1_000_000_000 + \
                        (after_ns - before_ns)
                    reaction_ms = round(reaction_ns / 1_000_000, 3)

                    return {
                        "success": True,
                        "reaction_ms": reaction_ms,
                        "reaction_ns": reaction_ns,
                        "error_code": match["error_code"],
                        "error_code_hex": match["error_code_hex"],
                        "details": match["details"],
                        "stamp_before": before_stamp,
                        "stamp_after": current_stamp,
                    }

                before_stamp = current_stamp
                before_sec, before_ns = self._parse_stamp(current_stamp)

            time.sleep(poll_interval)

        return {
            "success": False,
            "reaction_ms": None,
            "reaction_ns": None,
            "error_code": error_code,
            "error_code_hex": f"0x{error_code:08X}",
            "details": None,
            "stamp_before": before_stamp,
            "stamp_after": None,
        }

    def _nodes_in_error_code(self, error_code: int) -> list[str]:
        """
        details записи с данным error_code имеет вид {"nodes": [...]}.
        Возвращает список нод или [] если код не активен / не парсится.
        """
        match = next(
            (c for c in self.get_error_codes()
             if c["error_code"] == error_code),
            None
        )
        if match is None:
            return []
        try:
            return json.loads(match["details"]).get("nodes", [])
        except (ValueError, AttributeError):
            return []

    def wait_for_node_in_error_code(
        self,
        error_code: int,
        node_name: str,
        before_stamp: str = None,
        timeout: float = 10.0,
        poll_interval: float = 0.01
    ) -> dict:
        """
        Ждёт появления node_name в details.nodes записи с данным
        error_code (details -- JSON {"nodes": [...]}).

        В отличие от wait_for_error_code: сам факт наличия error_code в
        списке НЕ считается успехом -- код может быть уже активен из-за
        других, не связанных с этим тестом нод (watchdog агрегирует всех
        недоступных нод в одну запись). Успех -- только когда node_name
        реально появляется в списке.
        """
        if before_stamp is None:
            with self._lock:
                before_stamp = self._latest_stamp

        before_sec, before_ns = self._parse_stamp(before_stamp)
        start = time.time()

        while time.time() - start < timeout:
            with self._lock:
                current_stamp = self._latest_stamp

            if current_stamp != before_stamp:
                nodes = self._nodes_in_error_code(error_code)

                if node_name in nodes:
                    after_sec, after_ns = self._parse_stamp(current_stamp)
                    reaction_ns = (after_sec - before_sec) * 1_000_000_000 + \
                        (after_ns - before_ns)
                    reaction_ms = round(reaction_ns / 1_000_000, 3)

                    return {
                        "success": True,
                        "reaction_ms": reaction_ms,
                        "reaction_ns": reaction_ns,
                        "error_code": error_code,
                        "error_code_hex": f"0x{error_code:08X}",
                        "nodes": nodes,
                        "stamp_before": before_stamp,
                        "stamp_after": current_stamp,
                    }

                before_stamp = current_stamp
                before_sec, before_ns = self._parse_stamp(current_stamp)

            time.sleep(poll_interval)

        return {
            "success": False,
            "reaction_ms": None,
            "reaction_ns": None,
            "error_code": error_code,
            "error_code_hex": f"0x{error_code:08X}",
            "nodes": self._nodes_in_error_code(error_code),
            "stamp_before": before_stamp,
            "stamp_after": None,
        }

    def _parse_stamp(self, stamp: str) -> tuple[int, int]:
        """Парсит строку 'sec.nanosec' в два int."""
        if not stamp or "." not in stamp:
            return 0, 0
        parts = stamp.split(".")
        return int(parts[0]), int(parts[1])

    def stop(self):
        self._running = False
        if self._proc:
            self._proc.kill()
            self._proc.communicate()

    def get_error_codes(self) -> list[dict]:
        """
        Получить список error_codes из последнего сообщения.
        Возвращает список словарей с полями error_code и details.
        """
        with self._lock:
            raw = self._latest_raw

        codes = []
        current_code = None

        for line in raw.split("\n"):
            stripped = line.strip()
            clean = stripped.lstrip("- ")

            if clean.startswith("error_code:"):
                try:
                    current_code = int(clean.split(":")[1].strip())
                except ValueError:
                    current_code = None

            elif clean.startswith("details:") and current_code is not None:
                details = clean.split(":", 1)[1].strip().strip("'\"")
                codes.append({
                    "error_code": current_code,
                    "error_code_hex": f"0x{current_code:08X}",
                    "details": details,
                })
                current_code = None

        return codes

# import subprocess
# import threading
# import time


# class MrmRequestMonitor:
#     """
#     Читает /safety/mrm_request непрерывно в фоновом треде.
#     Один docker exec на весь сьют — нет SHM исчерпания.
#     """

#     def __init__(self, container: str):
#         self.container = container
#         self._latest_raw: str = ""
#         self._latest_stamp: str = ""  # ← sec.nanosec
#         self._lock = threading.Lock()
#         self._proc = None
#         self._thread = None
#         self._running = False
#         self._first_message = threading.Event()

#     def start(self):
#         cmd = [
#             "docker", "exec", self.container,
#             "bash", "-c",
#             "source /rep/ros2/install/setup.bash && "
#             "export ROS_DOMAIN_ID=1 && "
#             "ros2 topic echo /safety/mrm_request 2>/dev/null"
#         ]
#         self._proc = subprocess.Popen(
#             cmd,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.DEVNULL,
#             text=True,
#             bufsize=1
#         )
#         self._running = True
#         self._thread = threading.Thread(target=self._read_loop, daemon=True)
#         self._thread.start()

#     def _read_loop(self):
#         buffer = []
#         for line in self._proc.stdout:
#             if not self._running:
#                 break
#             if line.strip() == "---":
#                 raw = "\n".join(buffer)
#                 buffer = []
#                 if raw.strip():
#                     with self._lock:
#                         self._latest_raw = raw
#                         # Парсим stamp из сообщения
#                         sec = nanosec = None
#                         for l in raw.split("\n"):
#                             s = l.strip()
#                             if s.startswith("sec:"):
#                                 sec = s.split(":")[1].strip()
#                             elif s.startswith("nanosec:"):
#                                 nanosec = s.split(":")[1].strip()
#                         if sec and nanosec:
#                             self._latest_stamp = f"{sec}.{nanosec}"
#                     self._first_message.set()
#             else:
#                 buffer.append(line.rstrip())

#     def wait_ready(self, timeout: int = 15) -> bool:
#         ready = self._first_message.wait(timeout=timeout)
#         print(f"\n READY = {ready}")
#         return ready

#     def get_fields(self, fields: list[str]) -> dict:
#         with self._lock:
#             raw = self._latest_raw
#         result = {f: None for f in fields}
#         for line in raw.split("\n"):
#             stripped = line.strip()
#             for field in fields:
#                 if stripped.startswith(f"{field}:"):
#                     try:
#                         result[field] = stripped.split(":", 1)[1].strip()
#                     except IndexError:
#                         pass
#         return result

#     def get_stamp(self) -> str:
#         """Получить текущий timestamp последнего сообщения."""
#         with self._lock:
#             return self._latest_stamp

#     def wait_for_mrm_type_change(
#         self,
#         from_value: str,
#         to_value: str,
#         before_stamp: str = None,   # ← добавить параметр
#         timeout: float = 10.0,
#         poll_interval: float = 0.01
#     ) -> dict:
#         # Используем переданный stamp или берём текущий
#         if before_stamp is None:
#             with self._lock:
#                 before_stamp = self._latest_stamp

#         before_sec, before_ns = self._parse_stamp(before_stamp)
#         start = time.time()

#         while time.time() - start < timeout:
#             with self._lock:
#                 current_stamp = self._latest_stamp
#                 raw = self._latest_raw

#             if current_stamp != before_stamp:
#                 current_mrm = None
#                 for line in raw.split("\n"):
#                     stripped = line.strip()
#                     if stripped.startswith("mrm_type:"):
#                         current_mrm = stripped.split(":")[1].strip()
#                         break

#                 if current_mrm == to_value:
#                     after_sec, after_ns = self._parse_stamp(current_stamp)
#                     reaction_ns = (after_sec - before_sec) * 1_000_000_000 + \
#                         (after_ns - before_ns)
#                     reaction_ms = round(reaction_ns / 1_000_000, 3)

#                     return {
#                         "success": True,
#                         "reaction_ms": reaction_ms,
#                         "reaction_ns": reaction_ns,
#                         "mrm_type": current_mrm,
#                         "stamp_before": before_stamp,
#                         "stamp_after": current_stamp,
#                     }

#                 before_stamp = current_stamp
#                 before_sec, before_ns = self._parse_stamp(current_stamp)

#             time.sleep(poll_interval)

#         return {
#             "success": False,
#             "reaction_ms": None,
#             "reaction_ns": None,
#             "mrm_type": self.get_fields(["mrm_type"]).get("mrm_type"),
#             "stamp_before": before_stamp,
#             "stamp_after": None,
#         }

#     def wait_for_error_code(
#         self,
#         error_code: int,
#         before_stamp: str = None,
#         timeout: float = 10.0,
#         poll_interval: float = 0.01
#     ) -> dict:
#         """
#         Ждёт появления заданного error_code в error_codes сообщения
#         /safety/mrm_request (в отличие от wait_for_mrm_type_change,
#         не привязан к смене mrm_type — некоторые отказы могут не
#         эскалировать mrm_type, но добавлять запись в error_codes).
#         """
#         if before_stamp is None:
#             with self._lock:
#                 before_stamp = self._latest_stamp

#         before_sec, before_ns = self._parse_stamp(before_stamp)
#         start = time.time()

#         while time.time() - start < timeout:
#             with self._lock:
#                 current_stamp = self._latest_stamp

#             if current_stamp != before_stamp:
#                 match = next(
#                     (c for c in self.get_error_codes()
#                      if c["error_code"] == error_code),
#                     None
#                 )
#                 if match is not None:
#                     after_sec, after_ns = self._parse_stamp(current_stamp)
#                     reaction_ns = (after_sec - before_sec) * 1_000_000_000 + \
#                         (after_ns - before_ns)
#                     reaction_ms = round(reaction_ns / 1_000_000, 3)

#                     return {
#                         "success": True,
#                         "reaction_ms": reaction_ms,
#                         "reaction_ns": reaction_ns,
#                         "error_code": match["error_code"],
#                         "error_code_hex": match["error_code_hex"],
#                         "details": match["details"],
#                         "stamp_before": before_stamp,
#                         "stamp_after": current_stamp,
#                     }

#                 before_stamp = current_stamp
#                 before_sec, before_ns = self._parse_stamp(current_stamp)

#             time.sleep(poll_interval)

#         return {
#             "success": False,
#             "reaction_ms": None,
#             "reaction_ns": None,
#             "error_code": error_code,
#             "error_code_hex": f"0x{error_code:08X}",
#             "details": None,
#             "stamp_before": before_stamp,
#             "stamp_after": None,
#         }

#     def _parse_stamp(self, stamp: str) -> tuple[int, int]:
#         """Парсит строку 'sec.nanosec' в два int."""
#         if not stamp or "." not in stamp:
#             return 0, 0
#         parts = stamp.split(".")
#         return int(parts[0]), int(parts[1])

#     def stop(self):
#         self._running = False
#         if self._proc:
#             self._proc.kill()
#             self._proc.communicate()

#     def get_error_codes(self) -> list[dict]:
#         """
#         Получить список error_codes из последнего сообщения.
#         Возвращает список словарей с полями error_code и details.
#         """
#         with self._lock:
#             raw = self._latest_raw

#         codes = []
#         current_code = None

#         for line in raw.split("\n"):
#             stripped = line.strip()
#             clean = stripped.lstrip("- ")

#             if clean.startswith("error_code:"):
#                 try:
#                     current_code = int(clean.split(":")[1].strip())
#                 except ValueError:
#                     current_code = None

#             elif clean.startswith("details:") and current_code is not None:
#                 details = clean.split(":", 1)[1].strip().strip("'\"")
#                 codes.append({
#                     "error_code": current_code,
#                     "error_code_hex": f"0x{current_code:08X}",
#                     "details": details,
#                 })
#                 current_code = None

#         return codes