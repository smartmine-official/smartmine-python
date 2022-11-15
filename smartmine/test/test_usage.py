import os
import tempfile

from PIL import Image

import smartmine

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def test_login() -> None:
    smartmine.username = os.environ.get("SMARTMINE_USERNAME")
    smartmine.password = os.environ.get("SMARTMINE_PASSWORD")
    assert smartmine.username is not None
    assert smartmine.password is not None

    bearer_token = smartmine.login(username=smartmine.username, password=smartmine.password)
    assert isinstance(bearer_token, str)
    assert len(bearer_token) > 0


def test_process_image() -> None:
    original_image_path = f"{TEST_DIR}/testdata/smartmine_logo_large.png"
    original_image = Image.open(original_image_path)

    with tempfile.NamedTemporaryFile(suffix=".jpg") as f:
        smartmine.process_image(
            service_name=smartmine.ServiceName.image_enhancement,
            load_path=original_image_path,
            save_path=f.name,
        )

        # Check the image was saved successfully
        processed_image = Image.open(f.name)
        assert processed_image.size == original_image.size


def test_bulk_process_images() -> None:
    load_path = f"{TEST_DIR}/testdata"

    with tempfile.TemporaryDirectory() as temp_directory:
        smartmine.bulk_process_images(
            service_name=smartmine.ServiceName.image_enhancement,
            load_dir=load_path,
            save_dir=temp_directory,
        )

        # Check the images were saved successfully
        image_files = os.listdir(temp_directory)
        assert len(image_files) == 3
        for image_file in image_files:
            processed_image = Image.open(f"{temp_directory}/{image_file}")
            assert processed_image.size[0] > 0
            assert processed_image.size[1] > 0
