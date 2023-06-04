import sys
import socket
import string


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


def main():

    num_arg = len(sys.argv)
    if num_arg != 3:
        print("Invalid number of arguments provided")
        sys.exit(1)
    else:
        req_code = int(sys.argv[1])
        req_lim = int(sys.argv[2])
        server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_tcp_socket.bind(('', 0))
        _, n_port = server_tcp_socket.getsockname()
        print("SERVER PORT=" + str(n_port), flush=True)

        server_tcp_socket.listen(1)

        while True:
            client_socket, client_address = server_tcp_socket.accept()
            # print(f"Client connected from {client_address}", flush=True)

            cl_req_code = int(client_socket.recv(1024).decode('utf-8'))
            # print(f"The message received from client is: {cl_req_code}", flush=True)

            if cl_req_code == req_code:
                # Establish UDP socket connection since req_codes match
                server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                server_udp_socket.bind(('', 0))
                r_port = server_udp_socket.getsockname()[1]
                client_socket.send(str(r_port).encode('utf-8'))

                print("Connected via UDP")
                cl_msg_count = 1
                print(f"Req_lim = {req_lim}")
                while cl_msg_count <= req_lim:
                    print("Inside", flush=True)
                    print(f"Count: {cl_msg_count}", flush=True)
                    udp_msg, address = server_udp_socket.recvfrom(1024)
                    print(f"UDP Message: {udp_msg.decode('utf-8')}", flush=True)

                    # Check if string sent by client is a palindrome or not
                    result = check_pal(udp_msg.decode('utf-8'))
                    # Send back the result to the client
                    server_udp_socket.sendto(result.encode('utf-8'), address)

                    if udp_msg.decode('utf-8') == 'EXIT':
                        print("Received exit", flush=True)
                        break

                    if cl_msg_count == req_lim:
                        print("Inside the if check for req_lim", flush=True)
                        print("Reached limit", flush=True)
                        server_udp_socket.sendto("LIMIT".encode('utf-8'), address)
                        server_udp_socket.close()
                        break

                    cl_msg_count += 1

                server_udp_socket.close()
            else:
                print("Request Code does not match", flush=True)
                client_socket.send("Incorrect Req Code".encode('utf-8'))
                client_socket.close()
                sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)


