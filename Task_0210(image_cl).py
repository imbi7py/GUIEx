import socket
import numpy as np
import cv2

# Socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    buf = b''  # 정보를 얻기위해 바이트 문자열로 선언
    while count:
        newbuf = sock.recv(count) # sock.recv:소켓으로부터 데이터 읽을 때
        if not newbuf: return None # 받은 데이터 없으면 none
        buf += newbuf  # 받은 데이터 버퍼에
        count -= len(newbuf)  # 받은 데이터 개수 삭제
    return buf

HOST = '192.168.0.96'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # client 소켓 생성, IP4v와 TCP
client_socket.connect((HOST, PORT))  # IP주소와 port번호에 컨넥

while True:
    message = '1'
    client_socket.send(message.encode())   # 메세지인코드데이터 서버에게 전송

    length = recvall(client_socket, 16)   # recvall 함수 실행하여 buf 값 length에 넣기
    #길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를 먼저 받아서 이미지를 받을 때
    # 편리하려고 하는 것이다. 왜 16만 넣어야 동작하지???
    print(length)
    stringData = recvall(client_socket, int(length))
    # 받은이미지 str data로 변경
    data = np.frombuffer(stringData, dtype='uint8')
    #

    decimg = cv2.imdecode(data, 1) # 데이터 디코딩
    cv2.imshow('Image', decimg)

    key = cv2.waitKey(1)
    if key == 27:
        break

client_socket.close()