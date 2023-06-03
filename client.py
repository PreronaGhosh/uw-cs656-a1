import sys
import socket


def main():
    n = len(sys.argv)  # stores the number of command line arguments
    words = []  # list of all the strings passed in the command line argument

    if n < 5:
        print("Invalid arguments")
        sys.exit(1)
    else:
        server_address = sys.argv[1]
        n_port = int(sys.argv[2])
        req_code = sys.argv[3]
        # Add all the strings to words list
        for i in range(4, n):
            words.append(sys.argv[i])
        print(words)
        # Establish a connection to TCP Socket
        client_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_tcp_socket.connect((server_address, n_port))
        client_tcp_socket.send(req_code.encode('utf-8'))
        # print("Message sent to server")

        # Receive r_port from server
        r_port = client_tcp_socket.recv(1024).decode('utf-8')
        # print(f"r_port: {r_port}")
        client_tcp_socket.close()


if __name__ == '__main__':
    main()