from zlib import crc32, adler32
from hashlib import md5, sha1


class HashAlgos:
    algo_to_use = None

    @staticmethod
    def my_algo(string: str) -> int:
        hash_sum = 0
        for char in string:
            hash_sum <<= 1
            hash_sum += ord(char)
        return hash_sum & 0xFFFFFFFF

    @staticmethod
    def my_algo(string: str) -> int:
        hash_sum = 0
        for char in string:
            hash_sum <<= 1
            hash_sum += ord(char)
        return hash_sum & 0xFFFFFFFF

    @staticmethod
    def crc32(string: str) -> int:
        return crc32(string.encode())

    @staticmethod
    def adler32(string: str) -> int:
        return adler32(string.encode())

    @staticmethod
    def md5(string: str) -> int:
        return int(md5(string.encode()).hexdigest(), 16) & 0xFFFFFFFF

    @staticmethod
    def sha1(string: str) -> int:
        return int(sha1(string.encode()).hexdigest(), 16) & 0xFFFFFFFF

    @staticmethod
    def hash_str(string: str) -> int:
        return HashAlgos.algo_to_use(string)


HashAlgos.algo_to_use = HashAlgos.crc32
