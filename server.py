import sys
import socket


def main():
    n_port = 0
    num_arg = len(sys.argv)
    if num_arg != 3:
        print("Invalid arguments")
        exit(1)
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

            else:
                print("Inside else loop", flush=True)
                client_socket.close()


if __name__ == '__main__':
    main()