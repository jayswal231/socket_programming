import socket

s = socket.socket()
print("Socket created")

port = 12345

s.bind(('', port))
print(f"Socket binded to {port}")

s.listen(5)
print("Socket is listening...")

c, addr = s.accept()
print(f"Got connection from {addr}")

while True:
    # Receive message from client
    client_message = c.recv(1024).decode()
    if client_message.lower() == 'bye':
        print("Client disconnected.")
        break
    print(f"User: {client_message}")

    # Send message to client
    server_message = input("You: ")
    c.send(server_message.encode())
    if server_message.lower() == 'bye':
        print("Server disconnected.")
        break

c.close()
