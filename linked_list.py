class ObjList:
    def __init__(self, data: str):
        self.__data = data
        self.__prev = None
        self.__next = None

    def set_next(self, other):
        self.__next = other

    def get_next(self):
        return self.__next

    def set_prev(self, other):
        self.__prev = other

    def get_prev(self):
        return self.__prev

    def set_data(self, data: str):
        self.__data = data

    def get_data(self):
        return self.__data


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj: ObjList):
        if self.head is None:
            self.head = obj
        else:
            self.tail.set_next(obj)
            obj.set_prev(self.tail)
        self.tail = obj

    def remove_obj(self):
        if self.head is None:
            raise IndexError('list is empty')
        if (tail := self.tail.get_prev()):
            self.tail = tail
            self.tail.set_next(None)
        else:
            self.head = None

    def get_data(self):
        res = []
        obj = self.head
        while obj:
            res.append(obj.get_data())
            obj = obj.get_next()
        return res


# if __name__ == "__main__":
#     lst = LinkedList()
#     for i in range(4):
#         lst.add_obj(ObjList(f'data {i}'))
#     print(lst.get_data())
#     for _ in range(4):
#         lst.remove_obj()
#         print(lst.get_data())
#     lst.remove_obj()