import logging
from multiprocessing import Process
from typing import Optional

from gcp_storage_emulator.server import create_server

LOG = logging.getLogger(__name__)

_process: Optional[Process] = None

def _serve(host: str, port: int, in_memory: bool):
    server = create_server(host, port, in_memory)
    LOG.info("Starting local GCP Storage emulator on %s:%s", host, port)
    return server.start()

def start(host: str, port: int, in_memory: bool = False) -> Process:
    global _process
    if _process:
        return _process

    LOG.info("Starting local GCP Storage emulator on %s:%s", host, port)
    _process = Process(target=_serve, args=(host, port, in_memory), daemon=True)
    _process.start()
    return _process

def shutdown():
    global _process
    if not _process:
        return
    LOG.info("Shutting down local GCP Storage emulator")
    _process.stop()
    _process = None
