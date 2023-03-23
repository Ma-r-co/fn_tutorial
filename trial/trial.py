# %%
import xmltodict
import requests
from collections import defaultdict


# %%
def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


# %%
with open("./test_data.xml", "r") as f:
    in_xml = xmltodict.parse(f.read())
# %%
intA = in_xml["soapenv:Envelope"]["soapenv:Body"]["tem:Multiply"]["tem:intA"]
intB = in_xml["soapenv:Envelope"]["soapenv:Body"]["tem:Multiply"]["tem:intB"]

# %%
res_soap_data = recursive_defaultdict()
res_soap_data["soap:Envelope"][
    "@xmlns:soap"
] = "http://schemas.xmlsoap.org/soap/envelope/"
res_soap_data["soap:Envelope"][
    "@xmlns:xsi"
] = "http://www.w3.org/2001/XMLSchema-instance"
res_soap_data["soap:Envelope"]["@xmlns:xsd"] = "http://www.w3.org/2001/XMLSchema"
res_soap_data["soap:Envelope"]["soap:Body"]["MultiplyResponse"][
    "@xmlns"
] = "http://tempuri.org/"
res_soap_data["soap:Envelope"]["soap:Body"]["MultiplyResponse"]["MultiplyResult"] = int(
    intA
) * int(intB)


# %%
res_soap_data_xml = xmltodict.unparse(res_soap_data, pretty=True)
# %%
res_soap_headers = {"Content-Type": "application/xml, charset=utf-8"}
