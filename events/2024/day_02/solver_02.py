"""
Type: Challenge
Year: 2024
Day: 02 - Broken firewall
"""


def preprocessing(puzzle_input: str):
    """
    One (length, source IP, destination IP) tuple per hex packet.
    """
    packets: list[tuple[int, int, int]] = []
    for packet in puzzle_input.splitlines():
        packets.append(get_packet_details(packet))
    return packets


def solver(packets: list[tuple[int, int, int]]):
    """
    Total length of the packets going to or from the internal network, then
    to or from the wifi network, as 'internal/wifi'.
    """
    internal: int = 0
    wifi: int = 0
    for length, ip_from, ip_to in packets:
        if is_internal(ip_from) or is_internal(ip_to):
            internal += length
        if is_wifi(ip_from) or is_wifi(ip_to):
            wifi += length
    return f"{internal}/{wifi}"


def get_packet_details(packet: str):
    """
    Read the length, source IP and destination IP fields of a hex packet.
    """
    length = int(packet[4:8], 16)
    ip_from = int(packet[24:32], 16)
    ip_to = int(packet[32:42], 16)
    return length, ip_from, ip_to


def is_internal(ip: int) -> bool:
    """
    Whether the IP lies between 192.168.0.0 and 192.168.254.254.
    """
    return 3_232_235_520 <= ip <= 3_232_300_798


def is_wifi(ip: int) -> bool:
    """
    Whether the IP lies between 10.0.0.0 and 10.0.254.254.
    """
    return 167_772_160 <= ip <= 167_837_438
