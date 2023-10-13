import atexit
import logging

from localstack.extensions.api import Extension, http, services

LOG = logging.getLogger(__name__)


class LocalGCPStorageExtension(Extension):
    name = "localgcpstorage"

    backend_host = "localhost"
    backend_port = 9023
    in_memory = False

    def on_platform_start(self):
        # Start the local GCP Storage emulator when LocalStack starts
        from . import local_gcp_storage

        local_gcp_storage.start(self.backend_host, self.backend_port, self.in_memory)
        atexit.register(local_gcp_storage.shutdown)

    def update_gateway_routes(self, router: http.Router[http.RouteHandler]):
        # Add gateway routes for the GCP Storage emulator
        endpoint = http.ProxyHandler(f"http://{self.backend_host}:{self.backend_port}")

        # Add path routes for localhost:4566/gcp-storage
        router.add(
            "/gcp-storage",
            endpoint=endpoint,
        )

    def on_platform_shutdown(self):
        # Shutdown the local GCP Storage emulator when LocalStack is shutting down
        from . import local_gcp_storage

        local_gcp_storage.shutdown()
