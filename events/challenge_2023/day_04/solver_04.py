"""
Type: Challenge
Year: 2023
Day: 04 - MayDay
"""

from dataclasses import dataclass


@dataclass
class Packet:
    """
    Class describing a packet structure
    """
    header: str
    sender_number: int
    sequence_number: int
    checksum: int
    message: str

    @property
    def is_checksum_ok(self):
        """
        Checksum verification
        """
        computed_cs = sum(int(self.message[i: i + 2], 16)
                          for i in range(0, len(self.message), 2)) % 256
        return computed_cs == self.checksum


def preprocessing(
    puzzle_input: str
) -> list[Packet]:
    """
    Transforms raw input into Packets
    """
    packets: list[Packet] = []
    for line in puzzle_input.splitlines():
        packets.append(
            Packet(
                line[:4],
                int(line[4:12], 16),
                int(line[12:14], 16),
                int(line[14:16], 16),
                line[16:],
            )
        )
    return sorted(packets, key=lambda p: p.sequence_number)


def solver(packets: list[Packet]):
    """
    Extract the message from the received communications.
    """
    plaintext = ""
    for packet in packets:
        if packet.header != "5555" or not packet.is_checksum_ok:
            continue
        for i in range(0, len(packet.message), 2):
            plaintext += chr(int(packet.message[i:i+2], 16))
    return plaintext.strip()
