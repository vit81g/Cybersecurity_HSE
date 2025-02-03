from scapy.all import *
from scapy.layers.http import HTTPRequest , HTTPResponse, HTTP
from scapy.layers.inet import IP, TCP

dst_ip = "google-gruyere.appspot.com"
dst_port = 80

ip=IP(dst=dst_ip)
tcp=TCP(dport=dst_port)
http = HTTP() / HTTPRequest(Method="GET", Host=dst_ip, Path="/552739600875361128389016021534199822508")
send(ip/tcp/http)
response = sr1(ip / tcp / http, timeout=5)
if response:
    http_response = response[HTTPResponse]
    print(http_response.Status_Line)
    print(http_response.load)
else:
    print("No response received")