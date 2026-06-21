from abc import ABC, abstractmethod


class OCRAdapter(ABC):
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> str:
        pass
