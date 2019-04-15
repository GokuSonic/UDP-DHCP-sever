from socket import *

#data types
clients = []
ips = []
i =1
unassigned =[]
#populates the ip.list
while i !=255:
    unassigned.append(i)
    i+=1


client_counter =0


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ('The server is ready to receive')

def Discover():
    i = 0
    # the server checks the list whether the MAC address in the message exists in the list or not
    if client_mac in clients:
        print("Server: I see that the client with MAC address " + client_mac + " is discovering")

        for item in clients:
            print(item, "found at ", i, "in ", clients[i])
            # If a record was found, reply the client indicating that an
            # IP address x.x.x.x has already been assigned to this client
            print("ip has already been assigned")
            modifiedMessage = "DECLINE " +  ips[i]
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            i += 1

    # makes offer request
    else:
        # If no record was found for this client,
        # check whether the given pool of IP addresses has not been fully occupied by the current clients.
        # makes sure there are ips to assign to it
        if len(unassigned) != 0:
            new_ip = unassigned.pop()
            unassigned.append(new_ip)
            modifiedMessage = "OFFER " + "192.168.1." + str(new_ip) + " " + client_mac
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            print("client: received IP address 192.168.1." + str(new_ip))

        # If the whole pool of IP addresses is already occupied by the clients,
        # the server declines the request and replies a DECLINE message to the client.
        else:
            modifiedMessage = "DECLINE"
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            quit()


def Request():
    # gets the last 1-3 digits of the ip
    client_offer = (str(client_request_ip))[str(client_request_ip).rfind('.') + 1:len((str(client_request_ip)))]
    # debugging
    # print(client_offer)

    # check to see if the offered IP address is still available
    if client_offer in str(unassigned):
        # if YES:
        ##assigns IP address to the client and stores that
        # in it's list, then replies an ACKNOWLEDGE message
        # ontaining the clients MAC address and offered
        # IP address.
        unassigned.remove(int(client_offer))
        clients.append(client_mac)
        ips.append("192.168.1." + str(client_offer))
        modifiedMessage = "ACKNOWLEDGE " + client_mac + " " + "192.168.1." + str(client_offer)
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        print("Server: I assigned IP address 192.168.1." + str(client_offer) + " to this client")
    else:
        # if NO:
        # server offers new IP address to client
        print("new offer")
        if len(unassigned) != 0:
            new_ip = unassigned.pop()
            unassigned.append(new_ip)
            modifiedMessage = "OFFER " + "192.168.1." + str(new_ip) + " " + client_mac
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            print("Client: we have an IP address")

def Release():
    i = 0
    # the server checks the list whether the MAC address in the message exists in the list or not
    if client_mac in clients:
        print("Server: I see that the client with MAC address " + client_mac + " is releasing")

        # finds the record of the client and its assigned ip
        for item in clients:
            # IP address x.x.x.x has already been assigned to this client
            popped_ip = ips.pop(i)
            clients.pop(i)
            concat_ip = (str(popped_ip))[str(popped_ip).rfind('.') + 1:len((str(popped_ip)))]
            unassigned.append(int(concat_ip))
            modifiedMessage = "RELEASE " + popped_ip
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            i -= 1

    # no such assignment
    else:
        modifiedMessage = "SERVER:DECLINE"
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)


def Renew():
    i = 0
    # the server checks the list whether the MAC address in the message exists in the list or not
    if client_mac in clients:
        print("Server: I see that the client with MAC address " + client_mac + " is renewing")

        # finds the record of the client and its assigned ip
        for item in clients:
            # IP address x.x.x.x has already been assigned to this client
            popped_ip = ips.pop(i)
            ips.append(popped_ip)
            concat_ip = (str(popped_ip))[str(popped_ip).rfind('.') + 1:len((str(popped_ip)))]
            unassigned.append(concat_ip)

            modifiedMessage = "Server: Client already has IP address and the IP address is=" + popped_ip
            print(modifiedMessage)
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            i += 1

    # no such assignment
    else:
        if len(unassigned) != 0:
            new_ip = unassigned.pop()
            unassigned.append(new_ip)
            modifiedMessage = "OFFER " + "192.168.1." + str(new_ip) + " " + client_mac
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            print("renew: received IP address 192.168.1." + str(new_ip))


def Admin():
    # the server checks the password
    if str(client_mac) == "SuperSecretPa33w0rd!":
        print("password accepted")
        modifiedMessage = ""
        for client in clients:
            modifiedMessage += client + " "
        modifiedMessage += "/ "
        for IP in ips:
            modifiedMessage += IP + " "
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

    else:
        modifiedMessage = "NOT ADMIN"
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        print("password not accepted")

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)


    #gets message type and mac address
    #if the message is that of discover type
    if str(message).count(' ') == 1:
        type, client_mac = (message.decode()).split()
    #if the message is th format of request type
    elif str(message).count(' ') == 2:
        type, client_mac, client_request_ip = (message.decode()).split()
    else:
        modifiedMessage = "Invalid format--- try this:messagetype payload"
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)



    #DISCOVER
    if (str(type).upper()) == "DISCOVER":
       Discover()

    #REQUEST
    if (str(type).upper()) == "REQUEST":
       Request()


    #RELEASE
    if (str(type).upper()) == "RELEASE":
        Release()

    #RENEW
    if (str(type).upper()) == "RENEW":
       Renew()

    #RENEW
    if (str(type).upper()) == "ADMIN":
       Admin()


#print("Message tpe: ", type.decode())
# modifiedMessage =  "client " + message.decode() + " was added"
print(client_counter)
#serverSocket.sendto(modifiedMessage.encode(), clientAddress)
