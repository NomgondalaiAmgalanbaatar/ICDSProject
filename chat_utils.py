import socket
import time

# use local loop back address by default
# CHAT_IP = '127.0.0.1'
# CHAT_IP = socket.gethostbyname(socket.gethostname())
CHAT_IP = '127.0.0.1' # FIXED: explicitly set to localhost for Windows client compatibility

CHAT_PORT = 1112
SERVER = (CHAT_IP, CHAT_PORT)

menu = "\n++++ Choose one of the following commands\n \
        /time: calendar time in the system\n \
        /who: to find out who else are there\n \
        /connect <user>: to connect to the user and chat\n \
        /search <term>: to search your chat logs where <term> appears\n \
        /poem <#>: to get sonnet number <#>\n \
        /quit: to leave the chat system\n \
        @ai <query>: ask AI assistant\n \
        @<user>: mention a user\n\n"

S_OFFLINE   = 0
S_CONNECTED = 1
S_LOGGEDIN  = 2
S_CHATTING  = 3

SIZE_SPEC = 7  # Support up to 9,999,999 bytes (~10MB) for images

CHAT_WAIT = 0.2

def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_CHATTING:
        print('Chatting')
    else:
        print('Error: wrong state')

def mysend(s, msg):
    #append size to message and send it
    try:
        msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:] + str(msg)
        msg = msg.encode()
        total_sent = 0
        while total_sent < len(msg):
            sent = s.send(msg[total_sent:])
            if sent == 0:
                print('socket connection broken')
                return False
            total_sent += sent
        return True
    except Exception as e:
        print(f'mysend error: {e}')
        return False

def myrecv(s):
    #receive size first
    try:
        size = ''
        while len(size) < SIZE_SPEC:
            text = s.recv(SIZE_SPEC - len(size)).decode()
            if not text:
                print('disconnected')
                return('')
            size += text
        size = int(size)
        #now receive message
        msg = ''
        while len(msg) < size:
            text = s.recv(size-len(msg)).decode()
            if text == b'':
                print('disconnected')
                break
            msg += text
        #print ('received '+message)
        return (msg)
    except Exception as e:
        print(f'myrecv error: {e}')
        return ''

def text_proc(text, user):
    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    return('(' + ctime + ') ' + user + ' : ' + text) # message goes directly to screen
