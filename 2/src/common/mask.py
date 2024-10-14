from abc import ABC, abstractmethod

class IMask(ABC):

    @abstractmethod
    def mask(self) -> None:
        pass

    @abstractmethod
    def unmask(self) -> None:
        pass

    @abstractmethod
    def get_is_masked(self) -> bool:
        pass
