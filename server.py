import logging
import socket
import threading
import os
from typing import Union, List

log = logging.getLogger(__name__)


def handle_client(client_socket, port: int):
    peer = None
    try:
        peer = client_socket.getpeername()
        with client_socket:
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        log.info(f"No data on tcp handler {port}, closing connection...")
                        break
                    log.info(f"Echo back on tcp handler {port}: {data}")
                    client_socket.sendall(data)
            except Exception as e:
                log.error(f"Error on tcp handler {port}: {e}")
    except Exception as e:
        log.error(f"Error on tcp handler {port}: {e}")
    finally:
        log.info(f"Connection close on tcp handler {port}: {peer}")


def dgram_server(port: int) -> None:
    """
    Start a UDP echo server on the specified port
    :param port: The port to receive from
    :return: None
    """
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(("0.0.0.0", port))
        log.info(f"Waiting on udp port {port}")
        while True:
            # Wait for a datagram
            data, address = server.recvfrom(4096)
            log.info(f"Received udp data from {address} on {port}...")
            log.info(f"Echo back on udp handler {port}: {data}")
            server.sendto(data, address)
    except Exception as e:
        log.error(f"Error on udp handler {port}: {e}")


def stream_server(port: int) -> None:
    """
    Start a TCP echo server on the specified port
    :param port: The port to listen on
    :return: None
    """
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", port))
        server.listen(10)
        log.info(f"Listening on port {port}")
        while True:
            client_socket, addr = server.accept()
            log.info(f"Accepted connection from {addr} on {port}...")
            threading.Thread(target=handle_client, args=(client_socket,port)).start()
    except Exception as e:
        log.error(f"Error on listener {port}: {e}")


def get_ports(env: str) -> List[int]:
    if (not env in os.environ
            or os.environ[env] == ""
            or os.environ[env] == "0"
            or os.environ[env].lower() == "none"):
        log.info(f"{env} env not specified, specified, skipping them...")
    else:
        tcp = os.environ[env].split(",")
        return [int(p) for p in tcp]
    return []


def start_server_threads(type: str, ports: List[int], target: callable):
    threads = []
    for port in ports:
        log.info(f"Starting {type} Echo server on port {port}...")
        t = threading.Thread(target=target, args=(port,))
        t.daemon = True
        t.start()
        threads.append(t)
    return threads


def start_servers(port: Union[int, None], wait: bool=False) -> None:
    """
    Start one or more echo servers based on the port parameter and
    the TCPPORTS and UDPPORTS environment variables.

    If specified, the port parameter is always a TCP port

    :param port:
    :return:
    """
    tcp_ports = get_ports("TCPPORTS")
    if port is not None:
        tcp_ports.append(port)

    udp_ports = get_ports("UDPPORTS")

    if len(tcp_ports) == 0 and len(udp_ports) == 0:
        log.info("No TCP ports specified in PORT or TCPPORTS envvar and no UDP ports specifed in UDPPORTS, skipping...")
        return

    threads = []
    threads.extend(start_server_threads("TCP", tcp_ports, stream_server))
    threads.extend(start_server_threads("UDP", udp_ports, dgram_server))

    if wait:
        for t in threads:
            t.join()




