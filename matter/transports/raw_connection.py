import abc
import asyncio
import logging
import socket
import struct
import time
import uuid
from operator import itemgetter
from typing import Optional, Tuple

from more_itertools.recipes import first_true

from matter.transports.packages import ICMP, IP


class IRawConnection(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def _create_socket(family: int, proto: int): ...


class BaseRawConnection(IRawConnection):
    @staticmethod
    def _create_socket(family: int, proto: int):
        raise NotImplementedError

    @staticmethod
    def _create_id() -> int:
        return uuid.uuid4().int & 0xFFFF


class L2(BaseRawConnection):

    __sock_type__ = socket.SOCK_RAW

    def __init__(self, loop=None, host='127.0.0.1', port=0):
        self._loop = loop or asyncio.get_running_loop()

        self._buffer = 2048
        self._timeout = 10.0
        self._addr = host, port
        self._dst_address = None
        self._id = self._create_id()
        self._socket = self._create_socket(
            family=socket.AF_INET,
            proto=socket.getprotobyname('icmp'),
        )

    async def _resolve_addr(self, host, port):
        self._dst_address = await self.get_addr(host, port)

    @staticmethod
    def _create_socket(
            family: int = socket.AF_INET,
            proto: int = socket.IPPROTO_NONE,
    ) -> socket:
        return socket.socket(
            family=family,
            type=socket.SOCK_RAW | socket.SOCK_NONBLOCK,
            proto=proto,
        )

    async def get_addr(self, host: str, port: int) -> Optional[Tuple[str, int]]:
        sock_type_getter = itemgetter(1)
        dst_address_getter = itemgetter(4)

        info = first_true(
            iterable=await self._loop.getaddrinfo(host=host, port=port),
            default=None,
            pred=lambda _: sock_type_getter(_) == self.__sock_type__,
        )

        return info and dst_address_getter(info)

    def _sendto_ready(self, packet, future):
        self._socket.sendto(packet, self._dst_address)
        self._loop.remove_writer(self._socket)
        future.set_result(None)

    async def _send(self, packet):
        future = self._loop.create_future()
        self._loop.add_writer(self._socket, self._sendto_ready, packet, future)
        await future

    async def tick(self, packet):
        await self._send(packet)
        return await self._recv()

    async def _recv(self):
        try:
            return await asyncio.wait_for(
                self._loop.sock_recv(self._socket, self._buffer),
                timeout=self._timeout,
            )
        except asyncio.TimeoutError as e:
            logging.warning(e)
            return b''

    async def __aenter__(self):
        await self._resolve_addr(*self._addr)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()


# class L3(BaseRawConnection):
#     pass


def checksum(buffer):
    sum_ = 0
    count_to = (len(buffer) / 2) * 2
    count = 0

    while count < count_to:
        this_val = buffer[count + 1] * 256 + buffer[count]
        sum_ += this_val
        sum_ &= 0xffffffff
        count += 2

    if count_to < len(buffer):
        sum_ += buffer[len(buffer) - 1]
        sum_ &= 0xffffffff

    sum_ = (sum_ >> 16) + (sum_ & 0xffff)
    sum_ += sum_ >> 16
    answer = ~sum_
    answer &= 0xffff

    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def create_packet():
    checksum_ = 0
    id_ = uuid.uuid4().int & 0xFFFF

    header = struct.pack('BbHHh', 8, 0, checksum_, id_, 1)
    bytes_in_double = struct.calcsize('d')

    data = (192 - bytes_in_double) * 'A'
    data = struct.pack('d', time.time()) + data.encode('utf-8')

    checksum_ = checksum(header + data)

    header = struct.pack('BbHHh', 8, 0, socket.htons(checksum_), id_, 1)

    return header + data


async def main():
    packet = create_packet()

    async with L2() as connection:
        result = await connection.tick(packet)

    ip = IP.from_buffer(result)
    icmp = ICMP.from_buffer(result, ip.packet_length)
    print(icmp)


asyncio.run(main(), debug=True)
