from enum import Enum


class ServiceName(str, Enum):
    image_super_resolution = "image-super-resolution"
    image_deblurring = "image-deblurring"
    image_restoration = "image-restoration"
    image_denoising = "image-denoising"
