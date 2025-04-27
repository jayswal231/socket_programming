import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(f"\n{message}")
        except:
            break

# Setup client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

# Start receiving messages in a new thread
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

# Sending messages to the server
while True:
    message = input("You: ")
    
    if message.lower() == "bye":
        client.send(message.encode("utf-8"))
        client.close()
        break
    elif message.startswith("/private"):
        client.send(message.encode("utf-8"))
    else:
        # Public message
        client.send(message.encode("utf-8"))
