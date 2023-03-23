import io

# import json
import logging

# from lxml import etree
# from zeep import Client
import xmltodict
from collections import defaultdict

from fdk import response


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


# client = Client("http://www.dneonline.com/calculator.asmx?wsdl")
# node = client.create_message(client.service, "Multiply", intA=5, intB=5)


def handler(ctx, data: io.BytesIO = None):
    result = "<a>no data ingested<a>"
    try:
        in_xml = xmltodict.parse(data)
        intA = in_xml["soapenv:Envelope"]["soapenv:Body"]["tem:Multiply"]["tem:intA"]
        intB = in_xml["soapenv:Envelope"]["soapenv:Body"]["tem:Multiply"]["tem:intB"]
        res_soap_data = recursive_defaultdict()
        res_soap_data["soap:Envelope"][
            "@xmlns:soap"
        ] = "http://schemas.xmlsoap.org/soap/envelope/"
        res_soap_data["soap:Envelope"][
            "@xmlns:xsi"
        ] = "http://www.w3.org/2001/XMLSchema-instance"
        res_soap_data["soap:Envelope"][
            "@xmlns:xsd"
        ] = "http://www.w3.org/2001/XMLSchema"
        res_soap_data["soap:Envelope"]["soap:Body"]["MultiplyResponse"][
            "@xmlns"
        ] = "http://tempuri.org/"
        res_soap_data["soap:Envelope"]["soap:Body"]["MultiplyResponse"][
            "MultiplyResult"
        ] = int(intA) * int(intB)
        result = xmltodict.unparse(res_soap_data, pretty=True)
    except (Exception, ValueError) as ex:
        logging.getLogger().error("error parsing xml payload: " + str(ex))

    logging.getLogger().info("Inside Python Hello World function")
    return response.Response(
        ctx,
        response_data=result,
        headers={"Content-Type": "application/xml"},
    )
