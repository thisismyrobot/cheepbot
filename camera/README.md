# Web server to return images from a Pi camera.

## Setup

On the Pi, as tested in Python 3.5:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Running it

On the Pi, as tested in Python 3.5:

    ./serve.sh

## Accessing images

    http://[pi IP address]:10000/
