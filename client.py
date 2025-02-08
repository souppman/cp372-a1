import socket  # For network communication
import os      # For file operations when receiving files

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        # Initialize connection parameters
        self.host = host  # Server address (default is localhost)
        self.port = port  # Server port (default is 12345)

        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.clientSocket.connect((self.host, self.port)) # create TCP socket for server 

            # Get assigned client number from server
            client_num = self.clientSocket.recv(1024).decode()
            
            # Check if server is full
            if "Server is full" in client_num:
                print(f"\n{client_num}")
                self.clientSocket.close()
                raise Exception("Server is full")
                
            print(f"Client ID: Client{client_num}")

            # Format client name (e.g., Client01) and send to server
            name = f"Client{int(client_num):02d}"
            self.clientSocket.send(name.encode())

            # Display welcome message and available commands
            welcome_msg = self.clientSocket.recv(1024).decode()
            print("\n" + "="*50)
            print(welcome_msg)
            print("="*50 + "\n")
            print("Available commands:")
            print("- 'status': Get server status")
            print("- 'list': List available files")
            print("- 'get <filename>': Download a file")
            print("- 'exit': Disconnect from server")
            print("-"*50)

        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")
            if hasattr(self, 'clientSocket'):
                self.clientSocket.close()
            raise

    def receive_file(self, filename):
        """Stream and display file contents from the server"""
        try:
            print(f"\nContents of {filename}:")
            print("="*50)
            
            # Receive and display file contents
            data = self.clientSocket.recv(1024)
            if data.startswith(b'Error'):
                print(data.decode())
                return
                
            print(data.decode(), end='')
            print("\n" + "="*50)
            
        except Exception as e:
            print(f"Error receiving file: {str(e)}")

    def send_message(self):
        """Main loop for sending messages and handling commands"""
        try: 
            while True:
                try:
                    # Get user input and send to server
                    message = input("Enter your message: ") 
                    self.clientSocket.send(message.encode()) #sends message to server

                    # Handle different types of commands
                    if message.lower() == "exit":
                        # Clean disconnection from server
                        print("[CLIENT] Disconnecting...")
                        response = self.clientSocket.recv(1024).decode()  #receives response from server 
                        print(response)
                        break
                    elif message.lower() == "status":
                        # Get and display server's client cache
                        response = self.clientSocket.recv(1024).decode()
                        print("\nServer Status:")
                        print("-"*50)
                        print(response)
                        print("-"*50)
                    elif message.lower() == "list":
                        # Get and display available files
                        response = self.clientSocket.recv(1024).decode()
                        print("\nServer Repository:")
                        print("-"*50)
                        print(response)
                        print("-"*50)
                    elif message.lower().startswith("get "):
                        # Stream and display file contents
                        filename = message[4:].strip()
                        self.receive_file(filename)
                    else:
                        # Handle regular message (expect ACK)
                        response = self.clientSocket.recv(1024).decode()
                        print(f"Server response: {response}")
                except KeyboardInterrupt:
                    # Handle Ctrl+C gracefully
                    print("\n[CLIENT] Received interrupt, sending exit message...")
                    self.clientSocket.send("exit".encode())
                    try:
                        response = self.clientSocket.recv(1024).decode()
                        print(response)
                    except:
                        pass  # If server already closed, ignore receive error
                    break
        except Exception as e:
            print(f"\nERROR: {e}")
        finally:
            self.clientSocket.close()

    def start(self): 
        """Start the client and handle cleanup"""
        try:
            self.send_message()
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            # Ensure socket is closed even if errors occur
            if self.clientSocket:
                try:
                    self.clientSocket.close()
                except:
                    pass
            print("\nConnection closed.")

# Only run the client if this file is run directly
if __name__ == "__main__":
    try:
        client = ChatClient()
        client.start()
    except Exception as e:
        print(f"Failed to start client: {e}")