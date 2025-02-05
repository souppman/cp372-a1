# CP372 Assignment 1 - Client-Server Communication Application

## Overview
This is a Python-based client-server communication application developed for CP372 (Computer Networks) at Wilfrid Laurier University. The application implements a basic chat system between multiple clients and a server using TCP sockets.

## Group Members
- Jillian Fernandes
- Ryan Campbell 169073812 

## Features
- TCP socket-based client-server communication
- Support for multiple clients (up to 3 concurrent connections)
- Automatic client naming system (Client01, Client02, etc.)
- In-memory cache for tracking client connections
- Message acknowledgment system
- Status reporting functionality
- Clean client disconnection handling
- Bonus features:
  - File repository listing
  - File streaming capabilities

## Project Structure
```
.
├── README.md
├── Server.py
├── Client.py
└── Report.pdf
```

## Git Collaboration Guide

### First Time Setup
If you're setting up the repository for the first time:
```bash
# Clone the repository
git clone https://github.com/souppman/cp372-a1.git
cd cp372-a1

# Configure your Git identity (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add the remote repository
git remote add origin https://github.com/souppman/cp372-a1.git
```

### Making Changes
Follow these steps when making changes:
```bash
# Get the latest changes
git pull origin main

# Make your changes to the files

# Check status of your changes
git status

# Add your changes
git add .                  # Add all changes
# OR
git add specific_file.py   # Add specific file

# Commit your changes
git commit -m "Descriptive message about your changes"

# Push to repository
git push origin main
```

### Common Git Commands
- `git status`: Check status of your changes
- `git pull`: Get latest changes from repository
- `git add`: Stage changes for commit
- `git commit`: Save your changes locally
- `git push`: Upload your changes to repository
- `git log`: View commit history

### Best Practices
1. Always pull before making changes
2. Write clear commit messages
3. Test code before pushing

## Setup Instructions

### Running the Application
1. Start the server:
```bash
python server.py
```

2. Start a client (in a separate terminal):
```bash
python client.py
```

## Usage Instructions

### Server Commands
- The server automatically handles client connections and maintains a connection cache
- Server limits connections to 3 concurrent clients
- Server responds to client messages with acknowledgments

### Client Commands
- Messages are sent via command line interface
- Special commands:
  - `status`: Request current server cache contents
  - `exit`: Terminate connection with server
  - `list`: Request list of files in server repository (bonus feature)
  - To request a file: Enter the filename after receiving the file list

## Assignment Requirements
- Programming Language: Python
- Required Files:
  - Server.py
  - Client.py
  - Report.pdf
- Demonstration is mandatory
- Both team members' names must be included in code files and report

## Development Notes
- Server uses multi-threading to handle multiple clients
- Client naming follows the format "Client[XX]" (e.g., Client01, Client02)
- Cache maintains connection timestamps (start and end times)
- Clean disconnection handling implemented

## Testing
Refer to the Report.pdf for:
- Test cases and screenshots
- Implementation details
- Challenges faced and solutions
- Potential improvements
 