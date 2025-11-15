from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # truncate password to 72 bytes to avoid bcrypt error
    pw_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(pw_bytes)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(pw_bytes, hashed_password)
