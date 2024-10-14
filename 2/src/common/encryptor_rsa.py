from abc import ABC, abstractmethod
import rsa

class IEncryptorRSA(ABC):

    @abstractmethod
    def get_is_encrypted(self) -> bool:
        pass

    @abstractmethod
    def encrypt(self, public_key: rsa.PublicKey) -> None:
        pass

    @abstractmethod
    def decrypt(self, private_key: rsa.PrivateKey) -> None:
        pass