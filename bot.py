#!/usr/bin/python3

import sys
import time
import datetime
import socket
import ssl


# Connection config
host = 'irc.chat.twitch.tv'
port = 6697
channel = '#'

# Bot credentials
username = ''
token = 'oauth:'

# Social media
discord = 'https://discord.gg/'
donate_url = ''

# Commands
prefix = '!'
commands = {
    'discord': discord,
    'donate': donate_url,
    'ping': 'pong Kappa',
    'ding': 'dong Kappa'
}


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.wrap_socket(sock)

    print(f'Connecting to {host}:{port}...')
    try:
        sock.connect((host, port))
        print('Connection established!')
    except:
        print('Connection failed!')
        print('Exiting...')
        time.sleep(3)
        sys.exit()

    print(f'Attepting login to channel {channel}')
    sys_message(sock, f'PASS {token}')
    sys_message(sock, f'NICK {username}')
    sys_message(sock, f'JOIN {channel}')

    while True:
        try:
            for line in str(sock.recv(4096)).split('\\r\\n'):
                line = line.split(':', 2)

                if 'PING' in line[0]:
                    sys_message(sock, f'PONG :{line[1]}')

                elif len(line) > 2:
                    user = (line[1].split('!'))[0]
                    msg = line[2]
                    timestamp = datetime.datetime.now().strftime('%H:%M')

                    if msg[:len(prefix)] == prefix:
                        cmd = msg[len(prefix):].lower()

                        if cmd == 'commands':
                            send_message(sock, ', '.join(
                                [prefix + command for command in commands]))
                        elif cmd in commands:
                            send_message(sock, commands.get(cmd))

                    print(f'({timestamp}) {user}: {msg}')
        except:
            print('Lost connection, trying to reconnect.')
            main()


def send_message(sock, msg):
    sock.send(bytes(f'PRIVMSG {channel} :{msg}\r\n', 'utf-8'))


def sys_message(sock, msg):
    sock.send(bytes(f'{msg}\r\n', 'utf-8'))


if __name__ == '__main__':
    main()
