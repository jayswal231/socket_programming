import socket
import threading

# Dictionary to hold client addresses and their corresponding socket
clients = {}

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    
    # Add the client to the clients dictionary
    clients[client_address] = client_socket
    
    # Send a welcome message
    client_socket.send("Welcome to the chat! Type 'bye' to exit.".encode("utf-8"))

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                if message.lower() == "bye":
                    print(f"[{client_address}] disconnected.")
                    client_socket.send("You have left the chat.".encode("utf-8"))
                    client_socket.close()
                    del clients[client_address]  # Remove from clients when disconnecting
                    break

                print(f"[{client_address}] {message}")
                
                # Parse the message (e.g., send to another client)
                if message.startswith("/private"):
                    _, target_ip, target_port, *msg = message.split()
                    target_ip, target_port = target_ip, int(target_port)
                    msg = " ".join(msg)
                    
                    # Send the private message to the target client
                    send_private_message(target_ip, target_port, msg)
                else:
                    # Broadcast to all clients with "you:" and "friend:" labels
                    broadcast(message, client_socket)
            else:
                break
        except:
            break

    # Close connection when client disconnects
    client_socket.close()
    del clients[client_address]

# Function to broadcast message to all clients
def broadcast(message, client_socket):
    for client in clients.values():
        if client != client_socket:
            try:
                client.send(f"friend: {message}".encode("utf-8"))
            except:
                client.close()
                clients.remove(client)

# Function to send private message
def send_private_message(target_ip, target_port, message):
    target_client = None
    for address, client_socket in clients.items():
        if address == (target_ip, target_port):
            target_client = client_socket
            break
    
    if target_client:
        target_client.send(f"friend: {message}".encode("utf-8"))
    else:
        print(f"No client found at {target_ip}:{target_port}")

# Setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 5555))
server.listen(5)

print("[SERVER] Waiting for connections...")

# Accepting incoming client connections
while True:
    client_socket, client_address = server.accept()
    
    # Start a new thread to handle client communication
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()
