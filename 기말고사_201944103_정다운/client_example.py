import socket
import threading


def menual(): #메뉴얼
    print('*********************')
    print('* 도움말 단축키 /?    *')
    print('* 종료 단축키 /exit   *')
    print('*********************')

def exit():
    client_sock.close()

def Send(client_sock):
    try:
        my_name = input('user_name : ')  # 다른이에게 표시될 닉네임 설정
        send_data = bytes('{0}님이 접속하셨습니다 !'.format(my_name).encode())  # 해당 클라이언트의 접속을 다른 사용자에게 알림
        client_sock.send(send_data)  # 서버로 메세지 전송
        print('{0}님이 접속하셨습니다 !'.format(my_name))  # 이 클라이언트에게 표시할 내 접속 표시
        menual()  # 메뉴얼 표기
        try:
            while True: # 반복문을 돌며 exit를 만나기 전까지 메세지를 전송하기 위해 while문을 사용
                msg = input()  # 보낼 메세지 인풋
                if (msg == '/change'):  # 닉네임 변경
                    my_name = input('변경할 닉네임 입력 : ')
                if (msg == '/exit' or msg == '/EXIT'):  # 클라이언트 종료
                    exit()
                if (msg == '/?'):  # 메뉴얼 내 콘솔에 출력
                    menual()
                else:  # 기타 클라이언트에게 출력할 메세지를 서버로 전송
                    msg = my_name + ">> " + msg  # 클라이언트가 설정한 닉네임과 함께 메세지 전송
                    send_data = bytes(msg.encode())  # 보낼 메세지를 인코딩
                    client_sock.send(send_data)  # 인코딩된 메시지를 서버로 전송
        except:
            pass
    except ConnectionResetError:  # 서버에서 일방적으로 접속이 끊길 경우 해당 메세지 출력하며 클라이언트도 종료
        print('\n서버가 끊어졌습니다')
        exit()


def Recv(client_sock):  # 서버가 보낸 메세지를 받기 위해 해당 함수 사용
    try:
        while True:
            recv_data = client_sock.recv(1024).decode()  # 서버로부터 받은 메세지를 디코딩하여 내 화면에 출력
            print(recv_data)
    except ConnectionResetError:  # 서버에서 일방적으로 접속이 끊길 경우 해당 메세지 출력하며 클라이언트도 종료
        print('\n서버가 끊어졌습니다')
        exit()
    except ConnectionAbortedError:
        pass


try:
    # tcp 통신을 위하여 셋팅
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp socket
    Host = '127.0.0.1'  # 통신할 서버의 ip 주소
    Port = 9000  # 통신할 서버의 port 주소
    client_sock.connect((Host, Port))  # 서버로 연결시도
    print('연결된 서버 IP : {0}, PORT : {1} '.format(Host, Port))


    # client의 메세지를 보낼 쓰레드
    thread1 = threading.Thread(target=Send, args=(client_sock,))
    thread1.start()

    # server로부터 받은 다른 클라이언트의 메시지를 받을 쓰레드
    thread2 = threading.Thread(target=Recv, args=(client_sock,))
    thread2.start()
except ConnectionRefusedError:  # 서버가 동작하고 있지 않을 때 접속시도를 할경우 해당 메세지 출력
    print('서버 연결에 실패했습니다.')

