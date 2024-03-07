import re

line = '<14>Feb  8 10:01:18 ndm: Network::Interface::Mtk::WifiMonitor: "WifiMaster0/AccessPoint0": STA(c2:77:14:2f:b9:41) had associated.'


def extract_mac_address(text: str) -> str:
    """
    Функция извлекает MAC-адрес из заданного текста.

    Args:
      text: Строка, содержащая MAC-адрес.

    Returns:
      Строка с MAC-адресом.
    """
    # Регулярное выражение для поиска MAC-адреса
    pattern = r"(?:\(|\[)([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})(?:\)|\])"

    # Поиск MAC-адреса в тексте
    match = re.search(pattern, text)

    # Возвращение MAC-адреса, если он был найден
    if match:
        return str(match.group(0))[1:-1]

    # Возвращение пустой строки, если MAC-адрес не найден
    return ""

print(extract_mac_address(line))