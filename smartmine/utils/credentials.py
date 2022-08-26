from typing import Optional


def check_credentials(username: Optional[str], password: Optional[str]) -> None:
    if username is None or password is None:
        raise ValueError(
            'Please set the username and password using smartmine.username = "<username>" and smartmine.password = "<password>"'
        )
