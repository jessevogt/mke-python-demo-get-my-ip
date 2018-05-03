from asyncio import BaseEventLoop

import pytest
from aresponses import ResponsesMockServer, Response

from getmyip import get_ip, InconsistentIPAddressesFound
from services import TextService, JSONService


def test_getmyip_text_service(aresponses: ResponsesMockServer, event_loop: BaseEventLoop):
    aresponses.add('text.com', '/', 'GET', '1.2.3.4')
    assert get_ip([TextService('http://text.com')], event_loop) == '1.2.3.4'


def test_getmyip_json_service(aresponses: ResponsesMockServer, event_loop: BaseEventLoop):
    response = Response(body='{"ip": "1.2.3.5"}', content_type='application/json')
    aresponses.add('json.com', '/', 'GET', response)
    assert get_ip([JSONService('http://json.com', 'ip')], event_loop) == '1.2.3.5'


def test_getmyip_differing_ips(aresponses: ResponsesMockServer, event_loop: BaseEventLoop):
    aresponses.add('bad0.com', '/', 'GET', '1.2.3.6')
    aresponses.add('bad1.com', '/', 'GET', '1.2.3.7')

    with pytest.raises(InconsistentIPAddressesFound):
        get_ip([TextService('http://bad0.com'), TextService('http://bad1.com')], event_loop)

