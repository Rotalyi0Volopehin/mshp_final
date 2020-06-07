from zlib import crc32, adler32
from hashlib import md5, sha1


class HashAlgos:
    algos = None
    __current_algo_ind = 0

    @staticmethod
    def get_current_algo():
        return HashAlgos.algos[HashAlgos.__current_algo_ind]

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
        return HashAlgos.get_current_algo()(string)

    @staticmethod
    def try_next_algo() -> bool:
        print(f"Using of '{HashAlgos.get_current_algo().__name__}' hash algo failed")
        if len(HashAlgos.algos) - 1 == HashAlgos.__current_algo_ind:
            return False
        HashAlgos.__current_algo_ind += 1
        return True


HashAlgos.algos = [HashAlgos.crc32, HashAlgos.adler32, HashAlgos.md5, HashAlgos.sha1]
