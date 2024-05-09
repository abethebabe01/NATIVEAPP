import socket
import threading
import pyaudio

# Audio setup
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def client_handler(conn):
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            conn.sendall(data)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        conn.close()

def start_server():
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 2001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Listening on port {port}...")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            threading.Thread(target=client_handler, args=(conn,)).start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        server_socket.close()
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == '__main__':
    start_server()
