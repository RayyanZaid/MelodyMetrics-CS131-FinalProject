import zmq
import time
import os
import uuid

import datetime

import auralGlobals

from MusicPlayingGrading import testMusic

from playMidiFile import play_midi

# Function to receive a file from the server
def receive_file_and_string(socket, save_path):

    data = socket.recv_multipart()
    file_data = data[0]
    message_str = data[1].decode('utf-8')

    auralGlobals.sheetMusicName = message_str

    with open(save_path, 'wb') as f:
        f.write(file_data)
    print(f"File received and saved to {save_path} and string {message_str}")

# Set up ZMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.DEALER)  # DEALER socket for more complex communication
client_id = str(uuid.uuid4()).encode('utf-8')
socket.identity = client_id
socket.connect("tcp://192.168.7.191:5555")  # Connect to the server's port

print("Aural Nano client started, waiting for user command...")

while True:
    # Simulate user command
    user_command = input("Enter command (NEW_MUSIC/TEST/PLAY): ").strip().upper()

    if user_command == "NEW_MUSIC":
        # Send new music command to the server
        socket.send_multipart([client_id, b"NEW_MUSIC"])
        # Wait for the server's response (file data)

        print("Waiting say this with voice")
        receive_file_and_string(socket, "received_midi_file.mid")
        
        # Simulate waiting for user command for the next step
        time.sleep(2)

    elif user_command == "TEST":
        # Send test command to the server

        print("Send a voice command to tell the user to be seated and ready with correct posture in 4 seconds")

        time.sleep(4)

        testName = auralGlobals.sheetMusicName + "-" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        socket.send_multipart([client_id, b"TEST", testName.encode('utf-8')])
        

        # Call Wiiliam's stuff here
        # start_time = time.time()
        # duration = 20

        # while time.time() - start_time < duration:
        #     print("Grading music...")
        #     time.sleep(0.25)

        grade = testMusic()
        
        print(f"Saving Music Test data under test name : {testName}")
        print(f"Music graded: User1 got a {grade}%.")

        # Notify Visual Nano that the test is done
        socket.send_multipart([client_id, b"TEST_DONE"])
        print("Sent TEST_DONE signal to Visual Nano")

    elif user_command == "PLAY":
        
        
        print("Will play the music now")

        play_midi('received_midi_file.mid')
        print("Music played.")

    else:
        print("Invalid command.")
