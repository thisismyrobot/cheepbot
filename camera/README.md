# Web server to return images from a Pi camera.

![Example](test_image.jpg?raw=true "Example")

## Additional requirements

    sudo apt-get install python3-venv
    # Enable picam
    sudo raspi-config
    
## Setup

On the Pi, as tested in Python 3.5:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    chmod 755 serve.sh

## Running it

On the Pi, as tested with Python 3.5 on Raspbian Strech:

    ./serve.sh

## Accessing images

    http://[pi IP address]:10000/
