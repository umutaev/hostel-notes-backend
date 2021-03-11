from typing import List, Tuple


class Authenticate:
    def __init__(self, hard_coded_user_base: List[Tuple[str, str]]) -> None:
        self.users = hard_coded_user_base

    def check_user(self, username: str, token: str) -> bool:
        return next((item for item in self.users if item[0] == username), None) == token
