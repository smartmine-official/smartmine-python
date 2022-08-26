import tempfile
from pathlib import Path
from typing import List, Optional

from PIL import Image


def get_image_dimensions(load_path: str) -> List[int]:
    with Image.open(load_path) as img:
        width, height = img.size
    return [width, height]


def resize_image_and_save(
    load_path: str, new_width: int, new_height: int, save_path: Optional[str] = None
) -> str:
    with Image.open(load_path) as img:
        resized_img = img.resize((new_width, new_height))
        if save_path is None:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=Path(load_path).name
            ) as f:
                resized_img.save(f.name)
                return f.name
        else:
            resized_img.save(save_path)
