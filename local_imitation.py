class Data:
    __slots__ = ['data', 'ip']

    def __init__(self, data: str, ip: int):
        self.data = data
        self.ip = ip

    def __repr__(self):
        return f"Data {{message: {self.data}, send_to_ip: {self.ip}}}"


class Server:
    counter: int = 1

    def __init__(self):
        self.ip: int = self.__class__.counter
        self.__class__.counter += 1
        self.buffer: list[Data] = []
        self.router = None

    def send_data(self, data: Data):
        self.router.buffer.append(data)

    def get_data(self):
        return [self.buffer.pop() for _ in range(len(self.buffer))]

    def get_ip(self):
        return self.ip


class Router:
    def __init__(self):
        self.servers: dict[int, Server] = {}
        self.buffer: list[Data] = []

    def link(self, *servers: Server):
        for server in servers:
            self.servers[server.ip] = server
            server.router = self

    def unlink(self, server: Server):
        del self.servers[server.ip]
        server.router = None

    def send_data(self):
        while self.buffer:
            pack = self.buffer.pop()
            send_to = pack.ip
            self.servers[send_to].buffer.append(pack)


# if __name__ == "__main__":
    # router = Router()
    # sv_from = Server()
    # sv_from2 = Server()
    # router.link(sv_from, sv_from2, Server(), Server())
    # sv_from.send_data(Data('hello', sv_from2.get_ip()))
    # sv_from.send_data(Data('hello again', 2))
    # sv_from2.send_data(Data('hello again', 1))
    # print('router before: ', router.buffer)
    # print(sv_from2.buffer, sv_from.buffer)
    # router.send_data()
    # print('router after: ', router.buffer)
    # print('get data from server1: ', sv_from2.get_data())
    # print(sv_from2.buffer, sv_from.buffer)
