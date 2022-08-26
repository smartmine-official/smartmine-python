from smartmine.utils.model import ServiceName


def get_default_option_name(service_name: ServiceName) -> str:
    if service_name == ServiceName.image_super_resolution:
        return "upscaling-factor"
    elif service_name == ServiceName.image_deblurring:
        return "deblur-iterations"
    elif service_name == ServiceName.image_restoration:
        return "remove-scratches"
    elif service_name == ServiceName.image_denoising:
        return "denoising-strength"
    else:
        raise ValueError(f"Unsupported service: {service_name}")


def get_default_option_value(service_name: ServiceName) -> str:
    if service_name == ServiceName.image_super_resolution:
        return "2"
    elif service_name == ServiceName.image_deblurring:
        return "4"
    elif service_name == ServiceName.image_restoration:
        return "disabled"
    elif service_name == ServiceName.image_denoising:
        return "high"
    else:
        raise ValueError(f"Unsupported service: {service_name}")
