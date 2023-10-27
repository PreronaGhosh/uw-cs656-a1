
# Socket Programming with TCP & UDP

Simple program to explore socket programming using TCP and UDP sockets.




## Files

`server.py & client.py` : Python scripts to create a simple client-server program using TCP and UDP sockets.

`server.sh & client.sh` : Shell scripts for running Python programs. When executed, it will call the above mentioned python files.


## Compilation

    Not required as the programs are written in Python.


## Run Locally


To run the server

```bash
  ./server.sh <req_code> <req_lim>
```

To run the client

```bash
  ./client.sh <server_address> <n_port> <req_code> <msg_1> <msg_2> ... <msg_n>
```


## Parameters

To run this project, you will need to add the following parameters to your CLI commands/scripts: 

`<req_code>` : An integer validation code used by client and server

`<req_lim>` : Maximum number of strings that the server can process

`<server_address>` : The name/IP of the machine that the server is running on

`<n_port>` : The negotiation port printed out by the server

`<msg_n>` : The input message sent by the client to the server

## Machine Environments

The program has been run and tested on a Windows 11 machine, ubuntu2204-002 and ubuntu2204-004 on the Ubuntu student servers at the University of Waterloo.
