#!/usr/bin/python3

import socket
import ssl
import datetime

# Connection config
server_ip = ('irc.chat.twitch.tv', 6697)
channel = '#'

# Bot credentials
username = ''
token = 'oauth:'

# Social media
discord = 'https://discord.gg/'

# Commands
commands = {
    'discord': discord,
    'ping': 'pong Kappa',
    'ding': 'dong Kappa'
}


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.wrap_socket(sock)
    sock.connect(server_ip)
    sock.send(bytes('PASS ' + token + '\r\n', 'utf-8'))
    sock.send(bytes('NICK ' + username + '\r\n', 'utf-8'))
    sock.send(bytes('JOIN ' + channel + '\r\n', 'utf-8'))

    while True:
        for line in str(sock.recv(4096)).split('\\r\\n'):
            line = line.split(':', 2)

            if 'PING' in line[0]:
                sys_message(sock, f'PONG :{line[1]}')

            if len(line) > 2:
                user = (line[1].split('!'))[0]
                msg = line[2]
                msg_time = datetime.datetime.now().strftime('%H:%M')

                if msg[:1] == '!':
                    cmd = msg[1:].lower()

                    if cmd in commands:
                        send_message(sock, commands.get(cmd))

                print(f'({msg_time}) {user}: {msg}')


def send_message(sock, msg):
    sock.send(bytes(f'PRIVMSG {channel} :{msg}\r\n', 'utf-8'))


def sys_message(sock, msg):
    sock.send(bytes(f'{msg}\r\n', 'utf-8'))


if __name__ == '__main__':
    main()
