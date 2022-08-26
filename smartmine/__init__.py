import os
import re
import tempfile
from pathlib import Path
from typing import Optional

from tqdm import tqdm

from smartmine.utils.image import get_image_dimensions, resize_image_and_save
from smartmine.utils.model import ServiceName
from smartmine.utils.request import (
    login,
    get_request_token,
    upload_file,
    process_request,
    download_result,
    check_image_dimensions,
)
from smartmine.utils.credentials import check_credentials

username = None
password = None
bearer_token = None
api_base = "https://api.smartmine.net/api/v1"


def process_image(
    service_name: ServiceName, load_path: str, save_path: Optional[str] = None
):
    global bearer_token

    # Default to the user's Downloads folder if the save directory is not set
    if not save_path:
        save_path = str(Path.home() / "Downloads" / Path(load_path).name)

    check_credentials(username=username, password=password)
    bearer_token = login(username=username, password=password)
    _process_single_image(
        service_name=service_name, load_path=load_path, save_path=save_path
    )


def bulk_process_images(
    service_name: ServiceName, load_dir: str, save_dir: Optional[str] = None
):
    global bearer_token

    # Default to the user's Downloads folder if the save directory is not set
    if not save_dir:
        save_dir = str(Path.home() / "Downloads")

    # Get a list of the image files in the load directory
    files = [
        os.path.join(load_dir, f)
        for f in os.listdir(load_dir)
        if re.match(r".*\.(jpg|jpeg|png|JPG|JPEG|PNG)", f)
    ]
    if not files:
        raise FileNotFoundError(f"Found no JPEG or PNG files in {load_dir}")

    check_credentials(username=username, password=password)
    bearer_token = login(username=username, password=password)

    for load_path in tqdm(files, desc="Bulk processing images"):
        # Use the same filename as the input file when saving the result
        save_path = Path(save_dir) / Path(load_path).name
        _process_single_image(
            service_name=service_name, load_path=load_path, save_path=save_path
        )


def _process_single_image(
    service_name: ServiceName,
    load_path: str,
    save_path: str,
    upscale_result_to_match_source: bool = True,
):
    original_image_dimensions = get_image_dimensions(load_path)
    downsampled_load_path = _downsample_image_if_required(
        service_name=service_name, load_path=load_path
    )

    # If resizing back to the original file dimensions is enabled:
    #  (1) Process the down-sampled image
    #  (2) Down-sample the returned output before passing to the AI Image
    #      Upscaling service, if required
    #  (3) Upscale the processed image with the Upscaling service
    #  (4) Resize back to the original image size
    if (
        downsampled_load_path is not None
        and upscale_result_to_match_source
        and service_name != ServiceName.image_super_resolution
    ):
        with tempfile.NamedTemporaryFile(
            delete=True, suffix=Path(load_path).name
        ) as service_result:
            # Step (1)
            _upload_to_smartmine_and_download_result(
                service_name=service_name,
                load_path=downsampled_load_path,
                save_path=service_result.name,
            )
            with tempfile.NamedTemporaryFile(
                delete=True, suffix=Path(load_path).name
            ) as upscale_result:
                # Step (2)
                service_result_downsampled_load_path = _downsample_image_if_required(
                    service_name=ServiceName.image_super_resolution,
                    load_path=service_result.name,
                )
                # Step (3)
                _upload_to_smartmine_and_download_result(
                    service_name=ServiceName.image_super_resolution,
                    load_path=service_result_downsampled_load_path
                    if service_result_downsampled_load_path is not None
                    else service_result.name,
                    save_path=upscale_result.name,
                )
                # Step (4)
                resize_image_and_save(
                    load_path=upscale_result.name,
                    new_width=original_image_dimensions[0],
                    new_height=original_image_dimensions[1],
                    save_path=save_path,
                )
    # Otherwise, use the original image (or the down-sampled image, if required)
    else:
        _upload_to_smartmine_and_download_result(
            service_name=service_name,
            load_path=downsampled_load_path
            if downsampled_load_path is not None
            else load_path,
            save_path=save_path,
        )


def _upload_to_smartmine_and_download_result(
    service_name: ServiceName, load_path: str, save_path: str
) -> None:
    request_token = get_request_token(
        service_name=service_name, bearer_token=bearer_token
    )
    upload_file(
        service_name=service_name,
        file_path=load_path,
        bearer_token=bearer_token,
        request_token=request_token,
    )
    process_request(
        service_name=service_name,
        bearer_token=bearer_token,
        request_token=request_token,
    )
    download_result(
        service_name=service_name,
        save_path=save_path,
        bearer_token=bearer_token,
        request_token=request_token,
    )


def _downsample_image_if_required(service_name: ServiceName, load_path: str) -> str:
    # Check if the image has to be down-sampled
    downsampled_load_path = None
    original_image_dimensions = get_image_dimensions(load_path)
    new_dimensions = check_image_dimensions(
        service_name=service_name,
        image_width=original_image_dimensions[0],
        image_height=original_image_dimensions[1],
        bearer_token=bearer_token,
    )
    if new_dimensions is not None:
        downsampled_load_path = resize_image_and_save(
            load_path=load_path,
            new_width=new_dimensions[0],
            new_height=new_dimensions[1],
        )
    return downsampled_load_path
