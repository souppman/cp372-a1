import socket
import os
import threading
import datetime

class ChatServer:
    def __init__(self, host='localhost', port=12345, max_clients=3):
        self.host = host  # host is the ip address of the server
        self.port = port  # port is the port number of the server
        self.max_clients = max_clients  # max_clients is the maximum number of clients that can connect to the server
        self.clients = {}  # {client_id: (connection, address, start_time, end_time)}
        self.client_counter = 1  # client_counter is the number of clients that have connected to the server
        self.lock = threading.Lock()  # useful for thread safety and syncing client connections
        self.repository_path = "repository"

        # create repository directory if it doesn't exist
        if not os.path.exists(self.repository_path):
            os.makedirs(self.repository_path)

        # Initialize server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(max_clients)  # Queue up to max_clients connection requests

    def generate_client_id(self):
        """Generate a unique client number"""
        with self.lock:
            client_num = self.client_counter
            self.client_counter += 1
            return str(client_num)

    def handle_client(self, client_socket, client_address, client_num):
        """Handle individual client connections"""
        start_time = datetime.datetime.now() # get current time for client connection

        try:
            # Send client number and wait for client to send their formatted name
            client_socket.send(client_num.encode())
            client_id = client_socket.recv(1024).decode()
            
            # Store client information
            with self.lock:
                self.clients[client_id] = {
                    'socket': client_socket,
                    'address': client_address,
                    'start_time': start_time,
                    'end_time': None
                }

            # Send confirmation to client
            welcome_msg = f"Welcome {client_id}! You are now connected."
            client_socket.send(welcome_msg.encode())
            print(f"New client {client_id} connected from {client_address}")

            while True:
                # Receive message from client
                message = client_socket.recv(1024).decode()
                if not message:
                    break

                print(f"Received from {client_id}: {message}")  # Log received message

                # Handle special commands
                if message.lower() == "exit":
                    print(f"{client_id} requested to exit")
                    break
                elif message.lower() == "status":
                    status = self.get_client_status()
                    client_socket.send(status.encode())
                    print(f"Sent status to {client_id}")
                elif message.lower() == "list":
                    file_list = self.get_file_list()
                    client_socket.send(file_list.encode())
                    print(f"Sent file list to {client_id}")
                elif message.startswith("get "):
                    # Handle file transfer request
                    filename = message[4:].strip() # slice and strip to assure clean filename
                    print(f"{client_id} requested file: {filename}")
                    self.send_file(client_socket, filename)
                else:
                    # Echo message with ACK
                    response = f"{message} ACK"
                    client_socket.send(response.encode())
                    print(f"Sent to {client_id}: {response}")

        except Exception as e:
            print(f"Error handling client {client_id}: {str(e)}")
        finally:
            # Clean up client connection
            with self.lock:
                if client_id in self.clients:
                    self.clients[client_id]['end_time'] = datetime.datetime.now() # update end time for client connection
                    self.clients[client_id]['socket'].close()
                    print(f"Client {client_id} disconnected")

    def get_client_status(self):
        """Get status of all client connections"""
        status = "Current clients:\n" #status of current clients connected to server
        with self.lock:
            for client_id, info in self.clients.items(): #iterate through clients and add to status
                status += f"{client_id}:\n"
                status += f"  Address: {info['address']}\n"
                status += f"  Connected: {info['start_time']}\n"
                if info['end_time']: #if client has disconnected, add end time to status
                    status += f"  Disconnected: {info['end_time']}\n"
        return status

    def get_file_list(self):
        """Get list of files in repository"""
        try:
            files = os.listdir(self.repository_path) #list of files in repository
            if not files: 
                return "Repository is empty"
            return "Available files:\n" + "\n".join(files) #return list of files in repository
        except Exception as e:
            return f"Error accessing repository: {str(e)}" #error accessing repository

    def send_file(self, client_socket, filename): 
        """Send file to client"""
        filepath = os.path.join(self.repository_path, filename) #path to file in repository
        if not os.path.exists(filepath): 
            client_socket.send(f"Error: File '{filename}' not found".encode()) #error if file not found
            return

        try:
            with open(filepath, 'rb') as f: #open file in repository
                while True:
                    data = f.read(1024) #read 1024 bytes at a time
                    if not data:
                        break
                    client_socket.send(data) #send data to client
        except Exception as e:
            client_socket.send(f"Error sending file: {str(e)}".encode()) #error sending file

    def start(self):
        print(f"Server started on {self.host}:{self.port}") #print server started
        try:
            while True:
                client_socket, client_address = self.server_socket.accept() #accept client connection

                # Check if maximum clients reached
                if len(self.clients) >= self.max_clients:
                    client_socket.send("Server is full. Please try again later.".encode()) #send server is full
                    client_socket.close() #close client connection
                    continue

                client_num = self.generate_client_id() #generate client number
                print(f"New connection from {client_address[0]}:{client_address[1]}")

                # Start new thread for client handling
                client_thread = threading.Thread( #start new thread for client handling
                    target=self.handle_client, 
                    args=(client_socket, client_address, client_num) #pass client socket, address, and number
                )
                client_thread.daemon = True #doesn't block the main thread from exiting which kills all threads if server is closed 
                client_thread.start()  

        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()