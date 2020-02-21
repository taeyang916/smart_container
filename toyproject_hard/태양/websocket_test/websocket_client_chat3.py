# socket 모듈을 임포트
from socket import *
import sys


# 호스트, 포트와 버퍼 사이즈를 지정
HOST = '192.168.0.9'
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 객체를 만들고
clientSocket = socket(AF_INET, SOCK_STREAM)

# 서버와의 연결을 시도
try:
    clientSocket.connect(ADDR)
except Exception as e:
    print('채팅 서버(%s:%s)에 연결 할 수 없습니다.' % ADDR)
    sys.exit()
print('채팅 서버(%s:%s)에 연결 되었습니다.' % ADDR)
print('여기 ok')

# 채팅 메시지 띄우기
def prompt():
    sys.stdout.write('나>> ')
    sys.stdout.flush()

def send_message(message):
    clientSocket.send(message.encode())
    prompt()

## 여기 오류남
# data = clientSocket.recv(BUFSIZE).decode()
# print('여기도 ok')
# print('%s' % data)

prompt()
# # 서버로부터 메시지 전달 받기
# data = clientSocket.recv(BUFSIZE).decode()
data = ''

try:
    while True:
        if data:
            print()
            prompt()

            # 서버로부터 메시지 전달 받기
            data = clientSocket.recv(BUFSIZE).decode()
        else:
            # 메시지 입력 받기
            message = sys.stdin.readline()
            send_message(message)
            clientSocket.close()

except Exception as e:
    # 소켓 종료
    clientSocket.close()
    sys.exit()





