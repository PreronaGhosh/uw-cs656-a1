import sys
import socket


def main():
    n = len(sys.argv)  # stores the number of command line arguments
    words = []  # list of all the strings passed in the command line argument
    results = []  # list to store all results of palindrome check

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
        print(words)  # debug
        print(f"Length of words list: {len(words)}")  # debug
        # Establish a connection to TCP Socket
        client_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_tcp_socket.connect((server_address, n_port))
        client_tcp_socket.send(req_code.encode('utf-8'))
        # print("Message sent to server")

        # Receive r_port from server
        r_port = client_tcp_socket.recv(1024).decode('utf-8')
        print(f"r_port: {r_port}")
        client_tcp_socket.close()

        if r_port != "Incorrect Req Code":
            # Establish UDP connection on r_port for each word in list
            client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            limit_reached = 0
            for w in words:
                print("Sending a message", flush=True)
                client_udp_socket.sendto(w.encode('utf-8'), (server_address, int(r_port)))
                print("Sent a message to server", flush=True)

                server_msg = client_udp_socket.recvfrom(1024)[0].decode('utf-8')
                print(f"Server message: {server_msg}", flush=True)

                if server_msg == 'TRUE' or server_msg == 'FALSE':
                    results.append(server_msg)

                if server_msg == 'LIMIT':
                    limit_reached = 1
                    print("UDP Connection to client closed as LIMIT was received", flush=True)
                    results.append("Request limit reached")
                    break

            if limit_reached == 0:
                print("Sent EXIT to server")
                client_udp_socket.sendto("EXIT".encode('utf-8'), (server_address, int(r_port)))

            client_udp_socket.close()

        # Print the final results array
        final_res = ""
        for res in results:
            final_res += res + ", "
        final_res = final_res[:-2]  # remove comma and space
        print(final_res)


if __name__ == '__main__':
    main()