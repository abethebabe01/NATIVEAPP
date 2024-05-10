import socket

def receive_audio(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        try:
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                # Process data here (for testing, just print its size)
                print("Received data size:", len(data))
        except Exception as e:
            print("Error receiving data:", e)

if __name__ == '__main__':
    receive_audio('127.0.0.1', 50001)
