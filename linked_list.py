from typing import Optional


class ObjList:
    '''Object, which keeps data(string) and references to prev and next objects, if they exist'''
    __slots__ = ['__prev', '__next', '__data']

    def __init__(self, data: str):
        self.__data = data
        self.__prev: Optional["ObjList"] = None
        self.__next: Optional["ObjList"] = None

    @property
    def next(self) -> "ObjList":
        return self.__next

    @next.setter
    def next(self, other: "ObjList") -> None:
        self.__next = other

    @property
    def prev(self) -> "ObjList":
        return self.__prev

    @prev.setter
    def prev(self, other: "ObjList") -> None:
        self.__prev = other

    @property
    def data(self) -> str:
        return self.__data

    @data.setter
    def data(self, data: str) -> None:
        self.__data = data

    def __repr__(self):
        return self.data


class LinkedList:
    '''represents collection LinkedList of objects of class ObjList,has head and tail attributes, and includes next methods:
     - add_obj(obj) add to end
      - remove() - delete last element
      - get_data() - return list of data from all ObjList in collection'''
    def __init__(self):
        self.head: Optional["ObjList"] = None
        self.tail: Optional["ObjList"] = None

    def add_obj(self, obj: ObjList) -> None:
        if self.head is None:
            self.head = obj
        else:
            self.tail.next = obj
            obj.prev = self.tail
        self.tail = obj

    def remove_obj(self) -> None:
        if self.head is None:
            raise IndexError('list is empty')
        if tail := self.tail.prev:
            self.tail = tail
            self.tail.next = None
        else:
            self.head = None

    def get_data(self) -> list[ObjList.data]:
        res = []
        obj = self.head
        while obj:
            res.append(obj)
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
