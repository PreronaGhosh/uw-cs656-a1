import sys
import socket


# Method for TCP signalling phase for client
def create_tcp_socket(server_address, req_code, n_port):
    # Establish a connection to TCP Socket
    client_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_tcp_socket.connect((server_address, n_port))

    # Send the req_code to server for validation
    client_tcp_socket.send(req_code.encode('utf-8'))

    # Receive r_port from server
    r_port = client_tcp_socket.recv(1024).decode('utf-8')

    client_tcp_socket.close()
    return r_port


# Method to check the format of command line arguments
def check_format(arg):

    if len(arg) < 5:
        print("Invalid number of arguments provided")
        return 'NULL', 'NULL', 'NULL'
    else:
        server_address = arg[1]
        n_port = int(arg[2])
        req_code = arg[3]
        return server_address, n_port, req_code


def main():

    # Check the format of command line arguments
    server_address, n_port, req_code = check_format(sys.argv)

    if server_address == 'NULL' and n_port == 'NULL' and req_code == 'NULL':
        sys.exit(1)

    else:
        words = []  # list of all the strings passed in the command line argument
        results = []  # list to store all results of palindrome check

        # Add all the messages to the 'words' list
        for i in range(4, len(sys.argv)):
            words.append(sys.argv[i])

        # Create a TCP connection with server and get the r_port value
        r_port = create_tcp_socket(server_address, req_code, n_port)

        if r_port != "Incorrect Req Code":
            # Establish UDP socket on r_port for each message that has to be sent to the server
            client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            limit_reached = 0   # Flag variable - 1: Message Limit reached on server side, 0: Message Limit not reached

            for w in words:
                # Send messages to server one by one
                client_udp_socket.sendto(w.encode('utf-8'), (server_address, int(r_port)))

                # Check the result of palindrome check executed by the server on the message that was sent
                server_msg = client_udp_socket.recvfrom(1024)[0].decode('utf-8')

                # Store the result from server if there was a TRUE/FALSE return value
                if server_msg == 'TRUE' or server_msg == 'FALSE':
                    results.append(server_msg)

                # Condition will be fulfilled if server notifies client that message limit has been reached
                # Stop sending any more messages to server once message limit has been reached
                if server_msg == 'LIMIT':
                    limit_reached = 1
                    results.append("Request limit reached")
                    break

            # If message limit was not reached, then all messages were sent by client
            # Send EXIT signal to server
            if limit_reached == 0:
                client_udp_socket.sendto("EXIT".encode('utf-8'), (server_address, int(r_port)))

            client_udp_socket.close()
        else:
            print("Incorrect Request Code sent to server")
            sys.exit(1)

        # Print the final results array
        final_res = ""
        for res in results:
            final_res += res + ", "
        final_res = final_res[:-2]  # remove comma and space
        print(final_res)


if __name__ == '__main__':
    main()