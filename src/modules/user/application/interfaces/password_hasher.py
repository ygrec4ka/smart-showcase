from typing import Protocol


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        """Принимает сырой пароль, возвращает хеш"""
        ...

    def verify(self, password: str, hashed_password: str) -> bool:
        """Проверяет, соответствует ли сырой пароль хешу, возвращает булево значение"""
        ...
