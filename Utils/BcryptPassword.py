import bcrypt

class BcryptPassword:
    def hash_password(plain: str, PEPPER: str, BCRYPT_COST: int) -> str:       
        plain_peppered = (plain + PEPPER).encode("utf-8")

        salt = bcrypt.gensalt(rounds=BCRYPT_COST)

        pwd_hash = bcrypt.hashpw(plain_peppered, salt)

        return pwd_hash.decode("utf-8")  # Guardar como string en Mongo


    def verify_password(stored_hash: str, candidate: str, PEPPER: str) -> bool:       
        candidate_peppered = (candidate + PEPPER).encode("utf-8")

        return bcrypt.checkpw(candidate_peppered, stored_hash.encode("utf-8"))
