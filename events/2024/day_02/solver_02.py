"""
Type: Challenge
Year: 2024
Day: 02 - Solver 02
"""

def preprocessing(puzzle_input: str):
    packets: list[tuple[int, int, int]] = []
    for packet in puzzle_input.splitlines():
        packets.append(get_packet_details(packet))
    return packets


def solver(packets: list[tuple[int, int, int]]):
    q = 256 ** 3
    internal: int = 0
    wifi: int = 0
    for length, ip_from, ip_to in packets:
        print(ip_from, ip_to)
        if is_internal(ip_from) or is_internal(ip_to):
            internal += length
        if is_wifi(ip_from) or is_wifi(ip_to):
            wifi += length
    return f"{internal}/{wifi}"


def get_packet_details(packet: str):
    length = int(packet[4:8], 16)

    ip_from: list[int] = []
    ip_from_int = int(packet[24:32], 16)
    while ip_from_int:
        ip_from.insert(0, ip_from_int % 256)
        ip_from_int //= 256

    ip_to: list[int] = []
    int_ip_to = int(packet[32:42], 16)
    while int_ip_to:
        ip_to.insert(0, int_ip_to % 256)
        int_ip_to //= 256

    return length, ip_from, ip_to


def is_internal(ip: list[int]):
    print(ip)
    return ip[0] == 192 and ip[1] == 168 and 0 <= ip[2] <= 254 and 0 <= ip[3] <= 254


def is_wifi(ip: list[int]):
    return ip[0] == 10 and ip[1] == 0 and 0 <= ip[2] <= 254 and 0 <= ip[3] <= 254