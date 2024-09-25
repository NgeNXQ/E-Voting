from abc import ABC, abstractmethod

class IGammaEncryptor(ABC):

    @abstractmethod
    def get_is_encrypted(self) -> bool:
        raise NotImplementedError("get_is_encrypted is not implemented.")

    @abstractmethod
    def toggle_gamma_encryption(self, xor_key: bytes) -> None:
        raise NotImplementedError("toggle_gamma_encryption is not implemented.")