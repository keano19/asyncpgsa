from sqlalchemy import Column

class Record:
    __slots__ = ('row',)

    def __init__(self, row):
        self.row = row

    def __getattr__(self, item):
        if item and self.row:
            item = str(item)
            try:
                return self.row[item]
            except KeyError:
                try:
                    return getattr(self.row, item)
                except AttributeError:
                    return None
        return None

    def __getitem__(self, key):
        if isinstance(key, Column):
            key = key.name

        try:
            return self.__getattr__(key)
        except KeyError:
            return None

    def __bool__(self):
        return self.row is not None

    def get(self, key: str, default_value=None):
        attr = self.__getattr__(key)
        if attr:
            return attr
        else:
            return default_value


class RecordGenerator:
    __slots__ = ('data', 'iter')

    def __init__(self, data):
        self.data = data
        self.iter = iter(data)

    def __iter__(self):
        return self

    def __next__(self):
        return Record(next(self.iter))

    def __bool__(self):
        return bool(self.data)
