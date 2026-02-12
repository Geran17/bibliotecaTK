from typing import Protocol


class AppVisual(Protocol):
    def ejecutar(self) -> None:
        ...
