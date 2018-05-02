from abc import ABC, abstractmethod
from functools import lru_cache
from json.decoder import JSONDecodeError
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
        return f'<{self.__class__.__name__} ' \
               f'endpoint={self.endpoint}' \
               f'{" " + extra if extra else ""}>'


class TextService(Service):
    async def request(self, session: ClientSession) -> str:
        response: ClientResponse = await session.get(self.endpoint)
        return (await response.text()).strip()


class JSONService(Service):
    def __init__(self, endpoint: str, path: str):
        super().__init__(endpoint)
        self.path = tuple(path.split())

    async def request(self, session: ClientSession) -> str:
        headers = {'Accept': 'application/json'}
        response: ClientResponse = await session.get(self.endpoint,
                                                     headers=headers)
        try:
            payload = await response.json()
        except JSONDecodeError as ex:
            text = await response.text()
            raise Exception(f'Unable to parse {text}') from ex

        for p in self.path:
            payload = payload[p]

        return payload

    def __repr__(self):
        return super().__repr__(path=self.path)


_service_type_registry = {
    'text': TextService,
    'json': JSONService,
}


def parse_service(line: str) -> Service:
    endpoint, *extra = line.split(maxsplit=2)

    content_type = extra.pop(0) if extra else 'text'
    args = [extra.pop(0)] if extra else []

    if content_type in _service_type_registry:
        return _service_type_registry[content_type](endpoint, *args)

    raise Exception(f'Error parsing service definition: {line}')


@lru_cache()
def services() -> Iterable[Service]:
    with open('services.txt', 'r') as f:
        return tuple(parse_service(line) for line in f)
