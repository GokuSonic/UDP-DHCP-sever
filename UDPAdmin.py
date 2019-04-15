from socket import *
import re,uuid
from tkinter import *


serverName = 'server ip goes here'
serverPort = 12000
Macaddress =''
ip =''
macs=''
ips=''

def submit():
    #set up for first call
    global serverName , serverPort, Macaddress , ip,ips,macs
    serverName = str(textbox.get())
    serverPort = int(textbox2.get())
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    Macaddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    #discover
    message = "Admin SuperSecretPa33w0rd!"
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    macs, ips =(modifiedMessage.decode()).split("/")
    clearData()


def clearData():
    window.destroy()

# set up GUI for first portion
window = Tk()
window.geometry("250x200")
window.title("Admin")

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
window.geometry("550x300")
window.title("ADMIN")


#result box
resultBox = Text(window, width=30, height=33, wrap=WORD, bg="white")
resultBox.grid(row=1, column=3, sticky=E)
resultBox.insert('end', "MAC ADDRESSES" + '\n')

resultBox2 = Text(window, width=30, height=33, wrap=WORD, bg="white")
resultBox2.grid(row=1, column=6, sticky=E)
resultBox2.insert('end', "IP ADDRESSES" + '\n')

listMac = macs.split()
for mc in listMac:
    resultBox.insert('end', mc + '\n')

listIp = ips.split()
for ipi in listIp:
    resultBox2.insert('end', ipi + '\n')

window.mainloop()

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.close()