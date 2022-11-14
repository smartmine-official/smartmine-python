class ServerUnreachable(Exception):
    def __init__(self) -> None:
        self.message = "The Smartmine API is unavailable. Please try again later or contact info@smartmine.net"
        super().__init__(self.message)


class LoginError(Exception):
    pass


class ImageDimensionsCheckError(Exception):
    pass


class RequestTokenError(Exception):
    pass


class UploadError(Exception):
    pass


class ProcessingError(Exception):
    pass


class ProgressError(Exception):
    pass


class DownloadError(Exception):
    pass
