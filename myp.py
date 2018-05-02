import asyncio
from typing import Iterable

import aiohttp

from services import services, Service


async def _get_ip(service_list: Iterable[Service]) -> str:
    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(*[svc.request(session) for svc in service_list])

    ip_addresses = set(responses)
    if len(ip_addresses) == 1:
        return next(iter(ip_addresses))

    raise InconsistentIPAddressesFound(f'found differing ip addresses across services: {",".join(ip_addresses)}')


class InconsistentIPAddressesFound(Exception):
    pass


def get_ip(service_list: Iterable[Service] = None, *, loop: asyncio.BaseEventLoop = None) -> str:
    if service_list is None:
        service_list = services()

    if loop is None:
        loop = asyncio.get_event_loop()

    ip_task = _get_ip(service_list)
    ip = loop.run_until_complete(ip_task)
    return ip


def _main():
    print(get_ip())


if __name__ == '__main__':
    _main()
