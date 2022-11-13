from enum import Enum


class ServiceName(str, Enum):
    image_super_resolution = "image-super-resolution"
    image_deblurring = "image-deblurring"
    image_restoration = "image-restoration"
    image_denoising = "image-denoising"
    image_enhancement = "image-enhancement"


class ServiceStatus(str, Enum):
    """
    The status of the usage request being processed.
    """

    pending = "pending"
    in_progress = "in-progress"
    complete = "complete"
    failed = "failed"
