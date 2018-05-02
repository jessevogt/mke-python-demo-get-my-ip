import pytest
from aresponses import ResponsesMockServer, Response

from myp import get_ip, InconsistentIPAddressesFound
from services import TextService, JSONService


def test_myp_get_ip_text(aresponses: ResponsesMockServer, event_loop):
    """ TextService """


def test_myp_get_ip_json(aresponses: ResponsesMockServer, event_loop):
    """ JSONService """


def test_myp_bad_ip(aresponses: ResponsesMockServer, event_loop):
    """ Services returning differing IP addresses """
