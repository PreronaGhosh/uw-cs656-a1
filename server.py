import sys
import socket
import string


# Method to convert a string to lowercase, remove punctuations and check if a string is palindrome or not
# Input: string
# Output: Boolean value of True/False based on the check
def check_pal(s):
    s = s.strip().lower()
    for ch in s:
        s = s.replace(" ", "")
        if ch in string.punctuation:
            s = s.replace(ch, '')

    result = 'FALSE'

    if s == s[::-1]:
        result = 'TRUE'

    return result


# Method to create TCP and UDP sockets
# Input: String (type of socket that needs to be created)
# Return: tuple (UDP socket object, negotiation port number)
def create_socket(sock_type):
    if sock_type == 'TCP':
        server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_tcp_socket.bind(('', 0))
        _, n_port = server_tcp_socket.getsockname()
        return server_tcp_socket, n_port

    elif sock_type == 'UDP':
        server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_udp_socket.bind(('', 0))
        r_port = server_udp_socket.getsockname()[1]
        return server_udp_socket, r_port


# Method to check the command line argument format
# Input: sys.argv - all command line arguments
# Return: tuple (request code - int, request limit - int)
def check_format(arg):
    if len(arg) != 3:
        print("Invalid number of arguments provided")
        return 'NULL', 'NULL'

    else:
        code = int(arg[1])
        limit = int(arg[2])
        return code, limit


def main():

    req_code, req_lim = check_format(sys.argv)

    if req_code == 'NULL' and req_lim == 'NULL':
        sys.exit(1)

    else:
        server_tcp_socket, n_port = create_socket('TCP')
        print("SERVER PORT=" + str(n_port), flush=True)

        server_tcp_socket.listen(1)

        while True:
            # Opening up a new connection with the client
            client_socket, client_address = server_tcp_socket.accept()

            # Waiting to receive the request code from client on the TCP socket
            cl_req_code = int(client_socket.recv(1024).decode('utf-8'))

            if cl_req_code == req_code:
                # Establish UDP socket connection since req_codes match
                server_udp_socket, r_port = create_socket('UDP')
                client_socket.send(str(r_port).encode('utf-8'))

                # Start a counter to check if req_lim has been reached or not
                cl_msg_count = 1
                while cl_msg_count <= req_lim:
                    udp_msg, address = server_udp_socket.recvfrom(1024)

                    # Check if string sent by client is a palindrome or not
                    result = check_pal(udp_msg.decode('utf-8'))
                    # Send back the result to the client
                    server_udp_socket.sendto(result.encode('utf-8'), address)

                    # Check if client has sent 'EXIT' when it has sent all the messages
                    if udp_msg.decode('utf-8') == 'EXIT':
                        break

                    # Check if the request limit has been met on the server side, stop processing if true
                    if cl_msg_count == req_lim:
                        server_udp_socket.sendto("LIMIT".encode('utf-8'), address)
                        server_udp_socket.close()
                        break

                    cl_msg_count += 1

                # Close the UDP socket once the UDP phase is over
                server_udp_socket.close()
            else:
                # Request codes do not match so close the TCP connection with client
                client_socket.send("Incorrect Req Code".encode('utf-8'))
                client_socket.close()
                # sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)


