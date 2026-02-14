Remote Computer Control (TLS Secure)

Remote Computer Control is a secure client-server system written in Python that enables live screen streaming and remote input execution over an encrypted TLS connection.

This project was built for educational purposes to demonstrate networking, encryption, real-time data streaming, and multi-threaded architecture.

Overview

The system consists of two main components:

Server

Accepts incoming TLS connections

Receives compressed screen frames

Displays the remote screen using OpenCV

Sends control commands to the client

Client

Captures screenshots using PyAutoGUI

Compresses frames to JPEG format

Sends frames over a TCP connection

Executes received commands locally

Communication is secured using TLS (SSL) encryption.

Technologies Used

Python 3

socket

ssl (TLS encryption)

OpenCV

PyAutoGUI

NumPy

threading

Communication Protocol

The project uses a custom TCP framing protocol:

A 4-byte big-endian header that indicates payload length

The payload itself (JPEG frame or encoded command)

This ensures reliable reconstruction of transmitted data and avoids packet boundary issues.

Features

Encrypted TLS communication

Live screen streaming

Remote mouse movement

Remote mouse clicks

Remote keyboard typing

Hotkey execution (e.g., ctrl+shift)

Scroll control

Frame change detection optimization

Command rate limiting

Multi-threaded bidirectional communication

Installation

Install dependencies:

pip install -r requirements.txt

If you do not have a requirements file, install manually:

pip install pyautogui opencv-python numpy

TLS Certificate Generation

Generate a self-signed certificate before running the server:

openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem

Place cert.pem and key.pem in the same directory as server.py.

Running the Application

Start the server:

python server.py

Start the client:

python client.py

Make sure both sides use the correct IP address and port configuration.

Supported Commands

Examples of commands that can be sent from the server console:

move_mouse 300 400
click
type_text Hello World
scroll 10
ctrl+shift

Type exit to stop command mode.

Security Notice

This project:

Does not include authentication

Does not verify certificates

Is not production-ready

Should only be used on machines you own or have explicit permission to access

It is intended for networking and systems programming practice.

Possible Improvements

Mutual TLS verification

Authentication handshake

Video encoding (H264)

Differential frame transmission

Graphical control interface

WAN-ready secure deployment
