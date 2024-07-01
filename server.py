import logging
import socket
import threading
import os
from typing import Union

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
                        log.info(f"No data on handler {port}, closing connection...")
                        break
                    client_socket.sendall(data)
                    log.info(f"Echo back on handler {port}: {data}")
            except Exception as e:
                log.error(f"Error on handler {port}: {e}")
    except Exception as e:
        log.error(f"Error on handler {port}: {e}")
    finally:
        log.info(f"Connection close on handler {port}: {peer}")


def start_server(port: int) -> None:
    """
    Start a TCP echo servers on the specified port
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


def start_tcp_servers(port: Union[int, None], wait: bool=False) -> None:
    """
    Start one or more echo servers based on the port parameter and
    the TCPPORTS environment variables
    :param port:
    :return:
    """
    ports = []
    if port is not None:
        ports.append(port)
    if "TCPPORTS" in os.environ:
        if (os.environ["TCPPORTS"] == ""
                or os.environ["TCPPORTS"] == "0"
                or os.environ["TCPPORTS"].lower() == "none"):
            log.info("TCPPORTS env not specified, specified, skipping them...")
        else:
            tcp = os.environ["TCPPORTS"].split(",")
            ports.extend([int(p) for p in tcp])
    if len(ports) == 0:
        log.info("No TCP ports specified in PORT or TCPPORTS envvar, skipping them...")
        return

    threads = []
    for port in ports:
        log.info(f"Starting TCP Echo server on port {port}...")
        t = threading.Thread(target=start_server, args=(port,))
        t.daemon=True
        t.start()
        threads.append(t)
    if wait:
        for t in threads:
            t.join()
