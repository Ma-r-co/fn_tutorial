import fdk
import lxml
import pytest

from fdk import fixtures
from fdk import response

from pythonfn.func import handler


@pytest.mark.asyncio
async def test_parse_request_without_data():
    call = await fixtures.setup_fn_call(handler)

    content, status, headers = await call

    assert 200 == status
    assert "<a>no data ingested<a>" == content


@pytest.mark.asyncio
async def test_parse_request_with_data():
    req_headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tempuri.org/Multiply",
    }
    req_content = """<?xml version="1.0" encoding="utf-8"?>
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
                <soapenv:Header/>
                <soapenv:Body>
                    <tem:Multiply>
                        <tem:intA>5</tem:intA>
                        <tem:intB>3</tem:intB>
                    </tem:Multiply>
                </soapenv:Body>
                </soapenv:Envelope>"""
    call = await fixtures.setup_fn_call(
        handler, method="POST", headers=req_headers, content=req_content
    )

    content, status, headers = await call

    assert 200 == status
    assert "<a>no data ingested<a>" == content
