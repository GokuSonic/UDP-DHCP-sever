from socket import *
import re,uuid
from tkinter import *


serverName = 'server ip goes here'
serverPort = 12000
Macaddress =''
ip =''

def submit():
    #set up for first call
    global serverName , serverPort, Macaddress , ip
    serverName = str(textbox.get())
    serverPort = int(textbox2.get())
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    Macaddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    #discover
    message = "discover " + Macaddress
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    if str(modifiedMessage).count(' ') == 1:
        type, ip = (modifiedMessage.decode()).split()
        clearData()
    #if the message is th format of request type
    elif str(modifiedMessage).count(' ') == 2:
        type, ip, temp = (modifiedMessage.decode()).split()
        print(modifiedMessage.decode())

        #request
        message = "REQUEST " + Macaddress + " " + ip
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print(modifiedMessage.decode())

        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())
        clearData()


def clearData():
    window.destroy()

# set up GUI for first portion
window = Tk()
window.geometry("250x200")
window.title("Client")

serverLabel= Label(window,text ="Server IP")
serverLabel.pack(pady=2, padx=2)

serverName = StringVar()
textbox = Entry(window, textvariable=serverName)
textbox.focus_set()
textbox.pack(pady=10, padx=10)

serverPortLabel= Label(window,text ="Server Port")
serverPortLabel.pack(pady=2, padx=2)

serverPort = StringVar()
textbox2 = Entry(window, textvariable=serverPort)
textbox2.focus_set()
textbox2.pack(pady=10, padx=10)

subButton = Button(window, text="Submit", command=submit)
subButton.pack(pady=2, padx=2)

window.mainloop()




# set up GUI for second portion
window = Tk()
window.geometry("250x200")
window.title("Client")



def release():
    global serverName, serverPort, Macaddress, ip
    message = "RELEASE " + Macaddress
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    if str(modifiedMessage).count(' ') == 0:
        ip = '0.0.0.0'
        ipLabelText.set("Current Ip: " + ip)
        print(modifiedMessage.decode() , "Already released")
        # if the message is th format of request type
    elif str(modifiedMessage).count(' ') == 1:
        type, ip = (modifiedMessage.decode()).split()
        ip = '0.0.0.0'
        ipLabelText.set("Current Ip: " + ip)
        print(modifiedMessage.decode())


def renew():
    global serverName, serverPort, Macaddress, ip
    message = "RENEW " + Macaddress
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())

    if "=" not in modifiedMessage.decode():
        type, ip, temp = (modifiedMessage.decode()).split()

        # request
        message = "REQUEST " + Macaddress + " " + ip
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print( modifiedMessage.decode())

        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())
        ipLabelText.set("Current Ip: " + ip)


# add button release
Button(window, text="Release", width=8, bg="green", fg="white" , command= release).grid(row=0, column=10)

# add button renew
Button(window, text="Renew", width=8, bg="green", fg="white", command =renew).grid(row=1, column=10)

# button for quiting the program
Button(window, text="Quit", width=8, bg="green", fg="white", command=clearData).grid(row=2, column=10)

ipLabelText = StringVar()
ipLabel= Label(window,textvariable =ipLabelText)
ipLabel.grid(row=3, column=10)
ipLabelText.set("Current Ip: " + ip)

macLabelText = StringVar()
macLabel= Label(window,textvariable =macLabelText)
macLabel.grid(row=4, column=10)
macLabelText.set("Current Mac: " + Macaddress)
window.mainloop()

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.close()