import socket
import threading
from queue import Queue

# 서버에서 클라이언트로 메세지를 뿌려 주기 위해 해당 함수 이용
def Send(group, send_queue):
    while True:
        #새롭게 추가된 클라이언트가 있을 경우 Send 쓰레드를 새롭게 만들기 위해 루프를 빠져나감
        recv = send_queue.get()
        if recv == 'Group Changed':  # 새로운 send를 위하여 recv에 들어있는 문자열을 거르기 위해 사용
            break

        for conn in group:  #for 문을 돌면서 모든 클라이언트에게 메세지를 보내기 위해 for문 사용
            msg = str(recv[0])

            if recv[1] != conn:  # 클라이언트에서 보낸 메세지 본인이외의 클라이언트에게 메세지 출력
                conn.send(bytes(msg.encode()))
            else:  # 메세지가 비었을 때 패스
                pass

# 클라이언트에서 서버로 메세지 해독용도로 이용
def Recv(conn, count, send_queue):
    try:
        while True:
            data = conn.recv(1024).decode()  # 클라이언트에서 보낸 메세지 해독
            send_queue.put([data, conn, count]) #각각의 클라이언트의 메시지, 소켓정보, 쓰레드 번호를 send로 보냄
            print(str(addr)+'보냄 '+data)
    except ConnectionResetError:  # 클라이언트가 접속 끊겼을 때 오류방지용
        print(str(addr) + ' 접속종료')


# TCP Echo Server
send_queue = Queue()  # 클라이언트에서 보낸 정보를 잠시 저장하기 위해 사용
host = '' # 수신 받을 ip
port = 9000 # 수신받을 port
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP Socket
server_sock.bind((host, port)) # 소켓에 수신받을 ip와 port를 바인딩
server_sock.listen() # 소켓 연결
count = 0  # 클라이언트 접속수 카운트
group = [] #연결된 클라이언트의 소켓정보를 리스트로 묶기 위함
print('CHATTING SERVER ON')
while True:
    count = count + 1  # 접속수 카운팅
    conn, addr = server_sock.accept()  # 서버 소켓을 열고 준비
    group.append(conn)  # 연결된 클라이언트의 소켓정보를 group에 하나씩 저장
    print(str(addr) + ' 접속')  # 접속된 클라이언트 출력

    # 소켓에 연결된 모든 클라이언트에게 동일한 메시지를 보내기 위한 쓰레드(브로드캐스트)
    if count > 1:  # 카운트가 1이상이되면 새로운 클라이언트 정보를 받기 위해 변경된 group 리스트에 반영
        send_queue.put('Group Changed')  # 새로운 클라이언트 정보를 받을 준비로 체크 용도
        thread1 = threading.Thread(target=Send, args=(group, send_queue,))
        thread1.start()
        pass
    else:
        thread1 = threading.Thread(target=Send, args=(group, send_queue,))
        thread1.start()

    # 소켓에 연결된 각각의 클라이언트의 메시지를 받을 쓰레드
    thread2 = threading.Thread(target=Recv, args=(conn, count, send_queue,))
    thread2.start()
