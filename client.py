import socket

class ChatClient:
    def __init__ (self, host = 'localhost', port = 12345):
        self.host = host
        self.port = port 

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.clientSocket.connect((self.host,self.port)) # create TCP socket for server 


        client_num = self.clientSocket.recv(1024).decode() # receive client number from server 
        print(f"Client ID : Client{client_num}")

        name = input('Enter client name:')
        self.clientSocket.send(name.encode()) #send client name to server 

        welcome_msg= self.clientSocket.recv(1024).decode() # receive welcome message from server 
        print (welcome_msg)


    def send_message (self):
        try: 
            while True:
                message = input("Enter your message: ") 
                self.clientSocket.send(message.encode()) #sends message to server

                if message.lower() == "exit": # allows client to disconnect from server 
                    print("[CLIENT] Disconnecting...")
                    response = self.clientSocket.recv(1024).decode()  #receives response from server 
                    print(response)
                    break

                response = self.clientSocket.recv(1024).decode() # receive's server's response (message & ACK)
                print(f"Server response: {response}")
        except Exception as e:
            self.clientSocket.close()
    def start(self): 
        try:
            self.send_message()
        except Exception as e:
            print(f"ERROR {e}")
        finally:
            self.clientSocket.close()
            print(" Connection closed.")

if __name__ == "__main__":
    client = ChatClient()
    client.start()