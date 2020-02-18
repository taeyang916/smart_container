from socket import *
from select import *
import sys
from time import ctime

# 웹소켓 주소, 포트, 버퍼 사이즈 정의
HOST = '192.168.0.5'  # 주소는 공유기에 접속되 있는 ip 주소
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST, PORT)
flag = True

# 소켓 서버 초기화
serv = socket(AF_INET, SOCK_STREAM)
serv.close()

# 소켓 연결
server = socket(AF_INET, SOCK_STREAM)
# 주소 연결
server.bind(ADDR)
server.listen(10)
# 연결된 웹소켓 리스트
connection_list = [server]

print('==============================================')
print('채팅 서버를 시작합니다. %s 포트로 접속을 기다립니다.' % str(PORT))
print('==============================================')

client_socket, client_address = server.accept()
print('[INFO][%s] 클라이언트(%s)가 새롭게 연결 되었습니다.' % (ctime(), client_address[0]))
connection_list.append(client_socket)

# ==========현제 반복적으로 작동 안함==========
# 1회성으로 작동 중
try:
    while flag:
        if client_socket != server:
            # 클라이언트로 부터 소켓 정보 받아옴
            data = client_socket.recv(BUFSIZE).decode()
            print('hello :    %s' % str(data))

            # 데이터 존재 시
            if data:
                print('[INFO][%s] 클라이언트로부터 데이터를 전달 받았습니다.' % ctime())
                msg = 'Server got: ' + data
                # 연결된 모든 소켓에 메시지 전송
                client_socket.sendall(msg.encode())

            # 데이터 부재 시
            else:
                flag = False
                print('[INFO][%s] 사용자와의 연결이 끊어졌습니다.' % ctime())
                client_socket.close()
except Exception as e:
    # 웹 클라이언트 종료, 서버 종료
    client_socket.close()
    server.close()
