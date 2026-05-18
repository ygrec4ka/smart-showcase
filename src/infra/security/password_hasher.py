import bcrypt

from modules.user.application.interfaces import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)

        return hashed_bytes.decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        pwd_bytes = password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(
            password=pwd_bytes,
            hashed_password=hashed_bytes,
        )
