import socket
import select
import re
import base64
import hashlib
import struct
import sys
#
# from signal import signal, SIGPIPE, SIG_DFL
#
# signal(SIGPIPE, SIG_DFL)

global server
global input_list
global client_info

def send(input_list, msg):
    try:
        data = bytearray(msg.encode('utf-8'))
        # payload가 126일때 extended_payload_len을 2바이트 가지는데 이때 최대 값이 65535
        if len(data) > 65535:
            frame = bytearray([b'\x81', 127]) + bytearray(struct.pack('>Q', len(data))) + data
        elif len(data) > 125:
            frame = bytearray([b'\x81', 126]) + bytearray(struct.pack('>H', len(data))) + data
        else:
            frame = bytearray([b'\x81', len(data)]) + data
        # 클라이언트 리스트 모두에게 send ( 서버가 아니고 sys.stdin도 아닌 )
        for client in [sock for sock in input_list if not sock == server and not sock == sys.stdin]: client.sendall(
            frame)
    except Exception as e:
        print("send ERROR : " + str(e))


def recv(client):
    first_byte = bytearray(client.recv(1))[0]
    second_byte = bytearray(client.recv(1))[0]
    FIN = (0xFF & first_byte) >> 7
    opcode = (0x0F & first_byte)
    mask = (0xFF & second_byte) >> 7
    payload_len = (0x7F & second_byte)

    if opcode < 3:
        # payload_len 구하기
        if payload_len == 126:
            payload_len = struct.unpack_from('>H', bytearray(client.recv(2)))[0]
        elif payload_len == 127:
            payload_len = struct.unpack_from('>Q', bytearray(client.recv(8)))[0]
        # masking_key 구해서 masking된것 복구하기 ( mask가 1일 경우에만 존재 )
        if mask == 1:
            masking_key = bytearray(client.recv(4))
            masked_data = bytearray(client.recv(payload_len))
            data = [masked_data[i] ^ masking_key[i % 4] for i in range(len(masked_data))]
        else:
            data = bytearray(client.recv(payload_len))
    else:
        return opcode, bytearray(b'\x00')  # opcode 값을 넘김
    print(bytearray(data).decode('utf-8', 'ignore'))  # 받은거 콘솔에 출력용
    return opcode, bytearray(data)


def handshake(client):
    try:
        request = client.recv(2048)
        m = re.match('[\\w\\W]+Sec-WebSocket-Key: (.+)\r\n[\\w\\W]+\r\n\r\n', request)
        key = m.group(1) + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        response = "HTTP/1.1 101 Switching Protocols\r\n" + \
                   "Upgrade: websocket\r\n" + \
                   "Connection: Upgrade\r\n" + \
                   "Sec-WebSocket-Accept: %s\r\n" + \
                   "\r\n"
        r = response % ((base64.b64encode(hashlib.sha1(key).digest()),))
        client.send(r)
        print("---handshake end!---")
    except Exception as e:
        print("handshake ERROR : " + str(e))


def handler_client(client):
    try:
        opcode, data = recv(client)
        if opcode == 0x8:
            print('close frame received')
            input_list.remove(client)
            return
        elif opcode == 0x1:
            if len(data) == 0:
                # input_list.remove(client)
                # return
                print("emty data")
            else:
                # msg = data.decode('utf-8', 'ignore')
                msg = [c[1][0] + ":" + str(c[1][1]) for c in client_info if c[0] == client][0] + " :: " + data.decode(
                    'utf-8', 'ignore')
                # 클라이언트 리스트를 매개변수로 보냄
                send(input_list, msg)
        else:
            print('frame not handled : opcode=' + str(opcode) + ' len=' + str(len(data)))
    except Exception as e:
        print("handler ERROR : " + str(e))
        print("disconnected")
        input_list.remove(client)


def start_server(host, port):
    try:
        # host = '192.168.0.5'
        # port = 8000
        global server
        global input_list
        global client_info
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(0)
        input_list = [server, sys.stdin]  # sys.stdin은 쉘창에서 입력받은것 때문에 넣어줌
        client_info = []

        print("Server : " + host + ":" + str(port))
        while True:
            # select 함수는 관찰될 read, write, except 리스트가 인수로 들어가며
            # 응답받은 read, write, except 리스트가 반환된다.
            # input_list 내에 있는 소켓들에 데이터가 들어오는지 감시한다.
            # 다르게 말하면 input_list 내에 읽을 준비가 된 소켓이 있는지 감시한다.
            input_ready, write_ready, except_ready = select.select(input_list, [], [], 10)
            # 응답받은 read 리스트 처리
            for ir in input_ready:
                # 클라이언트가 접속했으면 처리함
                if ir == server:
                    client, addr = server.accept()
                    print("connected : " + str(addr))
                    handshake(client)
                    # input_list에 추가함으로써 데이터가 들어오는 것을 감시함
                    input_list.append(client)
                    client_info.append((client, addr))
                # 쉘 창 입력. 입력된 데이터 클라이언트에게 전송
                elif ir == sys.stdin:
                    send(input_list, "Administrator :: " + sys.stdin.readline())
                # 클라이언트소켓에 데이터가 들어왔으면
                else:
                    handler_client(ir)
    except Exception as e:
        print("start_server ERROR " + str(e))
        server.close()
        sys.exit()
    except KeyboardInterrupt:
        # 부드럽게 종료하기
        print("키보드 강제 종료")
        server.close()
        sys.exit()


start_server('192.168.0.5', 8000)