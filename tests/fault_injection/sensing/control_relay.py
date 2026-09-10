import requests

DEVICE_IP  = "192.168.1.120"
HTTP_PORT = "80"

API_LOGIN = "admin"
API_PASSWORD = "admin"

# Каналы реле -> лидар (подтверждено на стенде 2026-08-07).
# Канал rb15 (использовался в первой одноканальной версии теста) больше
# не актуален.
LIDAR_RELAY_CHANNELS = {
    4: "lidar_center_left",
    5: "lidar_left",
    6: "lidar_center",
    7: "lidar_right",
}

# Каналы реле -> радар (подтверждено на стенде 2026-08-24).
RADAR_RELAY_CHANNELS = {
    0: "radar_roof_back_left",
    1: "radar_roof_back_right",
    2: "radar_roof_front_right",
    3: "radar_roof_front_left",
}

# Каналы реле -> IMU (подтверждено 2026-09-04).
IMU_RELAY_CHANNELS = {
    8: "imu_ca",
    9: "imu_ch",
}


def relay_on(channel: int):
    """
    Разомкнуть цепь на канале `channel` -- физически СНИМАЕТ питание
    (имя функции не совпадает с эффектом, подтверждено на стенде
    2026-08-06/07 -- на этом блоке "on" размыкает, а не замыкает цепь).
    """
    url = f"http://{DEVICE_IP}/protect/rb{channel}n.cgi"
    response = requests.get(url, auth=(API_LOGIN, API_PASSWORD), timeout=5)
    return response


def relay_off(channel: int):
    """Замкнуть цепь на канале `channel` -- возвращает питание."""
    url = f"http://{DEVICE_IP}/protect/rb{channel}f.cgi"
    response = requests.get(url, auth=(API_LOGIN, API_PASSWORD), timeout=5)
    return response


if __name__ == "__main__":
    channel = int(input("Номер канала реле (4=lidar_center_left, 5=lidar_left, "
                         "6=lidar_center, 7=lidar_right): "))
    print(f"Включаем реле (канал {channel}) -- снимает питание")
    relay_on(channel)
    print("Готово")
    input("Нажмите Enter что бы выключить реле (вернуть питание)")
    print(f"Выключаем реле (канал {channel}) -- возвращает питание")
    relay_off(channel)
    print("Готово")
