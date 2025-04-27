import socket

s = socket.socket()

port = 12345

s.connect(('127.0.0.1', port))
print("Connected to server.")

while True:
    # Send message to server
    message = input("You: ")
    s.send(message.encode())
    if message.lower() == 'bye':
        print("Disconnected from server.")
        break

    # Receive reply from server
    server_reply = s.recv(1024).decode()
    if server_reply.lower() == 'bye':
        print("Server disconnected.")
        break
    print(f"Server: {server_reply}")

s.close()
