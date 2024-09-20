from sqlalchemy import inspect


class ReprMixin:
    __abstract__ = True

    __repr_attrs__ = []
    __repr_max_len__ = 50

    @property
    def _id_str(self):
        ids = inspect(self).identity
        if ids:
            return '-'.join(str(x) for x in ids)
        return 'None'

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_len__
        values = []
        for key in (set(self.__table__.columns.keys()) & set(self.__repr_attrs__)):
            value = getattr(self, key)
            if isinstance(value, str) and len(value) > max_length:
                value = f'{value[:max_length]} ...'
            values.append(f'{key} = {value}')
        return ' '.join(values)

    def __repr__(self):
        id_str = ('#' + self._id_str) or ''
        return f'<{self.__class__.__name__} {id_str} ({self._repr_attrs_str or ""})>'
