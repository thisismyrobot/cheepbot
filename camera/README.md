# Web server to return images from a Pi camera.

## Setup

On the Pi, as tested in Python 3.5:

    python3 -m venv venv
    source venv\scripts\activate
    pip install -r requirements.txt

## Running it

    python serve.py

## Accessing images

    http://[pi IP address]:10000/
