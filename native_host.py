import asyncio
import websockets
import pyaudio
import logging
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)

# Audio setup
CHUNK = 128
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()

# Function to get the IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't matter if the target is reachable
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = "127.0.0.1"
    finally:
        s.close()
    return ip_address

async def audio_stream(websocket, path):
    logging.info(f"Connection from {websocket.remote_address}")
    stream = None
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            await websocket.send(data)
    except (websockets.ConnectionClosedError, pyaudio.PyAudioError) as e:
        logging.error(f"Error: {e}")
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        logging.info("Stream and connection closed.")

async def main():
    ip_address = get_ip_address()
    logging.info(f"Server starting on {ip_address}:50001")
    server = await websockets.serve(audio_stream, '0.0.0.0', 50001)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
    p.terminate()
    logging.info("Server shutdown successfully.")
