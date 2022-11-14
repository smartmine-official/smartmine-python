from typing import Optional


def check_credentials(username: Optional[str], password: Optional[str]) -> None:
    if not username or not password:
        raise ValueError(
            'Please set the username and password using smartmine.username = "<username>" and smartmine.password = "<password>"'
        )
