from typing import Optional, TypeVar, Generic

T = TypeVar("T")


class SymbolTable(Generic[T]):
    parrent: Optional["SymbolTable"]
    symbols: dict[str, T]

    def __init__(
        self,
        parrent: Optional["SymbolTable"] = None,
    ):
        self.parrent = parrent
        self.symbols = {}

    def new_scope(self) -> "SymbolTable":
        return SymbolTable(parrent=self)

    def __setitem__(self, key: str, value: T):
        if key in self.symbols:
            raise KeyError(f"Symbol '{key}' already defined")

        self.symbols[key] = value

    def __getitem__(self, key: str) -> T:
        if key in self.symbols:
            return self.symbols[key]

        if self.parrent is not None:
            return self.parrent[key]

        raise KeyError(f"Symbol '{key}' not defined")

    def __len__(self) -> int:
        return len(self.symbols)
