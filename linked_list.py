class ObjList:
    __slots__ = ['__prev', '__next', '__data']

    def __init__(self, data: str):
        self.__data = data
        self.__prev = None
        self.__next = None

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, other):
        self.__next = other

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, other):
        self.__prev = other

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: str):
        self.__data = data


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj: ObjList):
        if self.head is None:
            self.head = obj
        else:
            self.tail.next = obj
            obj.prev = self.tail
        self.tail = obj

    def remove_obj(self):
        if self.head is None:
            raise IndexError('list is empty')
        if tail := self.tail.prev:
            self.tail = tail
            self.tail.next = None
        else:
            self.head = None

    def get_data(self):
        res = []
        obj = self.head
        while obj:
            res.append(obj.data)
            obj = obj.next
        return res


if __name__ == "__main__":
    lst = LinkedList()
    for i in range(4):
        lst.add_obj(ObjList(f'data {i}'))
    print(lst.get_data())
    for _ in range(4):
        lst.remove_obj()
        print(lst.get_data())
