# author: Michael Hüppe
# date: 10.05.2024
# project: bodyTracking_widget/resources/UnityCommunicator.py
import socket


class Distributor:
    """
    Distributes data to a local server
    """

    def __init__(self, address: str = "127.0.0.1", port: int = 5052):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address
        self.port = port

    def sendData(self, data: bytes):
        """
        Sends the data to the host
        :param data:
        :return:
        """
        self.conn.sendto(data, (self.address, self.port))