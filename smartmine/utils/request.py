import json
from typing import Dict, Any, Optional, List

import requests
from pathlib import Path

from smartmine.utils.model import ServiceName
from smartmine.utils.service import get_default_option_name, get_default_option_value
from smartmine.utils.exception import (
    LoginError,
    RequestTokenError,
    UploadError,
    ProcessingError,
    DownloadError,
    ProgressError,
)

API_V1_BASE_URL = "https://api.smartmine.net/api/v1"
API_V2_BASE_URL = "https://api.smartmine.net/v2"


def login(username: Optional[str], password: Optional[str]) -> str:
    assert username is not None
    assert password is not None

    url = f"{API_V2_BASE_URL}/login"
    response = requests.post(
        url=url, data=json.dumps({"username": username, "password": password})
    )
    response_content = response.json()
    if response.status_code != 200:
        raise LoginError(response.text)
    return response_content["content"]


def check_image_dimensions(
    service_name: ServiceName, image_width: int, image_height: int, bearer_token: str
) -> Optional[List[int]]:
    url = f"{API_V1_BASE_URL}/service/{service_name.value}/check-image-dimensions"

    payload = {
        "dimensions": {"width": image_width, "height": image_height},
        "usage_selection": _get_usage_selection(service_name),
    }
    response = requests.post(
        url=url,
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {bearer_token}"},
    )
    response_content = response.json()
    if response.status_code != 200:
        raise LoginError(response.text)
    if response_content["message"] == "Image requires resize":
        return [response_content["width"], response_content["height"]]


def get_request_token(service_name: ServiceName, bearer_token: str) -> str:
    url = f"{API_V2_BASE_URL}/service/request-token"

    response = requests.post(
        url=url,
        params={"service": service_name.value, "quantity": 1},
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        },
    )
    response_content = response.json()
    if response.status_code != 200:
        raise RequestTokenError(response.text)
    return response_content["content"]["request_token"]


def upload_file(file_path: str, bearer_token: str, request_token: str) -> None:
    url = f"{API_V2_BASE_URL}/service/upload"

    with open(file_path, "rb") as f:
        response = requests.post(
            url=url,
            files=[("file", (Path(file_path).name, f, "multipart/form-data"))],
            headers={
                "Authorization": f"Bearer {bearer_token}",
                "request-token": request_token,
                "input-name": "input__0",
            },
        )
        if response.status_code != 200:
            raise UploadError(response.text)


def process_request(bearer_token: str, request_token: str) -> None:
    url = f"{API_V2_BASE_URL}/service/process"

    response = requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
            "request-token": request_token,
        },
    )
    if response.status_code != 200:
        raise ProcessingError(response.text)


def get_progress(bearer_token: str, request_token: str) -> Dict[str, Any]:
    url = f"{API_V2_BASE_URL}/service/progress"

    response = requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
            "request-token": request_token,
        },
    )
    if response.status_code != 200:
        raise ProgressError(response.text)
    return response.json()["content"]


def download(save_path: str, bearer_token: str, request_token: str) -> None:
    url = f"{API_V2_BASE_URL}/service/download"

    response = requests.post(
        url=url,
        headers={
            "Authorization": f"Bearer {bearer_token}",
            "request-token": request_token,
            "output-name": "output__0",
        },
    )
    if response.status_code != 200:
        raise DownloadError(response.text)

    with open(save_path, "wb") as f:
        f.write(response.content)


def _get_usage_selection(service_name: ServiceName) -> Dict[str, Any]:
    """
    TODO deprecate along with API v1
    """
    return {
        "service_options_selection": [
            {
                "service_name": service_name.value,
                "option_name": get_default_option_name(service_name),
                "option_value": get_default_option_value(service_name),
            }
        ],
        "units_used": 1,
    }
