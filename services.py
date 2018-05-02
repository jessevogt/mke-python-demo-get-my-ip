from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Iterable

from aiohttp import ClientSession, ClientResponse


class Service(ABC):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @abstractmethod
    async def request(self, session: ClientSession) -> str:
        """ make request to service and parse response """

    def __repr__(self, **kwargs):
        extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
        return f'<{self.__class__.__name__} endpoint={self.endpoint}{" " + extra if extra else ""}>'


class TextService(Service):
    async def request(self, session: ClientSession) -> str:
        response: ClientResponse = await session.get(self.endpoint)
        return (await response.text()).strip()


class JSONService(Service):
    def __init__(self, endpoint: str, path: str):
        super().__init__(endpoint)
        self.path = tuple(path.split())

    async def request(self, session: ClientSession) -> str:
        response: ClientResponse = await session.get(self.endpoint, headers={'Accept': 'application/json'})
        payload = await response.json()

        for p in self.path:
            payload = payload[p]

        return payload

    def __repr__(self):
        return super().__repr__(path=self.path)


@lru_cache()
def parse_service(line: str) -> Service:
    endpoint, *args = line.split(maxsplit=2)

    content_type = args.pop(0) if args else 'text'
    param = args.pop(0) if args else None

    kwargs = {}

    if content_type == 'text':
        service_cls = TextService
    elif content_type == 'json':
        service_cls = JSONService
        kwargs['path'] = param
    else:
        raise Exception(f'Unknown service in line: {line}')

    return service_cls(endpoint, **kwargs)


@lru_cache()
def services() -> Iterable[Service]:
    with open('services.txt', 'r') as f:
        return tuple(parse_service(line) for line in f)
