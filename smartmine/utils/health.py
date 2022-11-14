import requests

from smartmine.utils.exception import ServerUnreachable
from smartmine.utils.request import API_V2_BASE_URL


def check_api_health() -> None:
    try:
        response = requests.get(f"{API_V2_BASE_URL}/health")
        assert response.status_code == 200
    except Exception:
        raise ServerUnreachable()
