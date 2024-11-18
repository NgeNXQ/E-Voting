class DatabaseService[TId, TEntry]:

    def __init__(self) -> 'DatabaseService':
        self._data: dict[TId, TEntry] = dict()

    def get_entries_count(self) -> int:
        return len(self._data)

    def get_entry(self, id: TId) -> TEntry:
        return self._data.get(id, None)

    def add_entry(self, entry: TEntry) -> None:
        if entry is None:
            raise ValueError("entry cannot be None")

        self._data[self._next_id] = entry

    def remove_entry(self, id: TId) -> None:
        if id not in self._data.keys():
            raise ValueError("Invalid id value")

        self._data.pop(id)
