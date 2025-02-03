
from scapy.all import *
from scapy.layers.http import HTTPRequest , HTTPResponse, HTTP
from scapy.layers.inet import IP, TCP
def http_callback(packet):
    if HTTPRequest in packet:
        http_layer = packet[HTTPRequest]
        print(f"Requested {http_layer.Method.decode()} {http_layer.Path.decode()}")

sniff(filter="port 80", prn=http_callback, store=0)