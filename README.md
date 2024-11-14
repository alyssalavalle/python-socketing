**Chat Application (Client-Server Model)**

Course: COMPE-560 - Computer and Data Networks\n
Institution: San Diego State University

This project implements a simple client-server chat application using Python’s socket programming and threading. The server relays messages between multiple clients in real-time, allowing them to communicate with each other.

**Table of Contents**

	1.	Project Overview
	2.	Requirements
	3.	File Descriptions
	4.	Usage Instructions
	5.	Features
	6.	Additional Notes

**Project Overview**

This chat application allows multiple clients to connect to a central server and send messages that are broadcast to all other connected clients. The server handles multiple clients concurrently, ensuring real-time message exchange. Clients can connect, send messages, and disconnect gracefully.

**Requirements**

	•	Python 3.x
	•	Socket module (built into Python standard library)
	•	Basic understanding of threading in Python

**File Descriptions**

	•	server.py: The server-side code responsible for handling client connections, managing message broadcasting, and handling disconnections.
	•	client.py: The client-side code that connects to the server, allows users to send messages, receive broadcasts, and gracefully disconnect.

**Usage Instructions**

1. Running the Server

	1.	Open a terminal window.
	2.	Navigate to the directory containing server.py.
	3.	Run the server with the command:

_python server.py_


	4.	The server will start listening on the specified IP and port (default: 127.0.0.1:12345).

2. Running the Clients

	1.	Open a new terminal window for each client that you wish to connect to the server.
	2.	Navigate to the directory containing client.py.
	3.	Run each client with the command:

_python client.py_

4.	Each client will connect to the server and be able to send and receive messages.

3. Using the Client Commands

	•	Send a Message: Type your message and press Enter to send it to all connected clients.
	•	Quit: Type quit and press Enter to disconnect gracefully from the server.

**Example Workflow**

	1.	Start the server with python server.py.
	2.	Open a new terminal and start a client with python client.py.
	3.	In the client terminal, type a message and press Enter to send it.
	4.	Open additional terminal windows and start more clients as needed. Messages will appear in real-time across all clients.

**Features**

	•	Multi-Client Support: The server can handle multiple clients simultaneously using threads.
	•	Real-Time Messaging: Messages are broadcast to all connected clients in real time.
	•	Graceful Disconnection: Clients can type quit to disconnect cleanly without affecting others.

**Additional Notes**

	•	This implementation is a command-line interface and does not include a graphical user interface (GUI).
	•	The server must be started before clients can connect.
	•	Default settings are configured for localhost (127.0.0.1). If testing across different devices, ensure all devices are on the same network and adjust IP settings accordingly.

**Bonus Features (Optional)**

The following features could be added for extra functionality:
	•	User Authentication: Prompt users for a username and password.
	•	Private Messaging: Allow clients to send direct messages to specific users.
	•	File Transfer Capabilities: Enable file sharing between clients.
