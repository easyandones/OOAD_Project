import hashlib


class Utils:
    @staticmethod
    def getHash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()