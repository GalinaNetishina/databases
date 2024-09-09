from collections import namedtuple, deque

Data = namedtuple('Data', ['text', 'ip'])


class Server:
    counter: int = 1

    def __init__(self):
        self.ip: int = self.__class__.counter
        self.__class__.counter += 1
        self.buffer: deque[Data] = deque()
        self.router = None

    def send_data(self, data: Data) -> None:
        self.router.buffer.append(data)

    def get_data(self):
        while self.buffer:
            yield self.buffer.popleft().text

    def get_ip(self) -> int:
        return self.ip


class Router:
    def __init__(self):
        self.servers: dict[int, Server] = {}
        self.buffer: deque[Data] = deque()

    def link(self, *servers: list[Server]) -> None:
        for server in servers:
            self.servers[server.ip] = server
            server.router = self

    def unlink(self, server: Server) -> None:
        try:
            del self.servers[server.ip]
            server.router = None
        except Exception:
            raise

    def send_data(self) -> None:
        while self.buffer:
            pack = self.buffer.popleft()
            send_to = pack.ip
            self.servers[send_to].buffer.append(pack)


servers = [Server() for _ in range(3)]
data = [Data(f'message #{i}', i % len(servers)) for i in range(1, 5)]
r = Router()
r.link(*servers)
servers[0].send_data(data[0])
servers[0].send_data(data[1])
servers[2].send_data(data[3])
print(r.buffer)
r.send_data()
for s in servers:
    print(f'server #{s.get_ip()} received: ', *s.get_data())
