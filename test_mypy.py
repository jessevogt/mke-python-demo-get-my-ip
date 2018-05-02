import pytest
from aresponses import ResponsesMockServer, Response

from myp import get_ip, InconsistentIPAddressesFound
from services import TextService, JSONService


def test_myp_get_ip_text(aresponses: ResponsesMockServer, event_loop):
    aresponses.add('text.com', '/', 'GET', '1.2.3.4')
    assert get_ip([TextService('http://text.com')], loop=event_loop) == '1.2.3.4'


def test_myp_get_ip_json(aresponses: ResponsesMockServer, event_loop):
    aresponses.add('json.com', '/', 'GET',
                   Response(body='{"ip": "1.2.3.5"}', content_type='application/json'))
    assert get_ip([JSONService('http://json.com', 'ip')], loop=event_loop) == '1.2.3.5'


def test_myp_bad_ip(aresponses: ResponsesMockServer, event_loop):
    aresponses.add('good.com', '/', 'GET', '1.2.3.6')
    aresponses.add('bad.com', '/', 'GET', '1.2.3.7')

    with pytest.raises(InconsistentIPAddressesFound) as ex:
        get_ip([
            TextService('http://bad.com'),
            TextService('http://good.com'),
        ], loop=event_loop)
