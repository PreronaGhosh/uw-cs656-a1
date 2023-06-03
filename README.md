CS 656 - Computer Networks - Spring 2023
Assignment 1 - Socket Programming
Prerona Ghosh 
Student ID: 21048873


Files:
1. server.py and client.py are Python scripts to create a simple client-server program using TCP and UDP sockets.
2. server.sh and client.sh are scripts modified for running Python programs. When executed, will call the above mentioned python files.
3. There is no Makefile provided as the programs are written in Python.


Compilation:
1. Not required as the programs are written in Python.


Execution steps:
To run the server, execute command: ./server.sh <req_code> <req_lim>
To run the client, execute command: ./client.sh <server_address> <n_port> <req_code> <msg_1> <msg_2> ... <msg_n>


Parameters:
<req_code>          : An integer validation code used by client and server.
<req_lim>           : Maximum number of strings that the server can process.
<server_address>	: The name/IP of the machine that the server is running on.
<n_port> 	  		: The negotiation port printed out by the server.
<msg> 		  	    : The input message sent by the client to the server.




