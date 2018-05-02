from asyncio import BaseEventLoop

import pytest
from aresponses import ResponsesMockServer, Response

from getmyip import get_ip, InconsistentIPAddressesFound
from services import TextService, JSONService


# def test_getmyip_text_service(aresponses: ResponsesMockServer, event_loop: BaseEventLoop):


# def test_getmyip_json_service(aresponses: ResponsesMockServer, event_loop: BaseEventLoop):


# def test_getmyip_differing_ips(aresponses: ResponsesMockServer, event_loop: BaseEventLoop):
