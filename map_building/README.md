# Map building off images.

![Combined](combined.png?raw=true "Combined")

## Setup

As tested with Python 3.6 on Windows:

    py -m venv venv
    venv\Scripts\activate.bat
    pip install -r requirements.txt

On the Pi, as tested in Python 3.5:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    chmod 755 serve.sh

## Running it

As tested with Python 3.6 on Windows:

    venv\Scripts\activate.bat
    python -m mapbuilder.serve

On the Pi, as tested in Python 3.5:

    ./serve.sh

## API

Test page:

    http://[pi IP address]:10001/

### API:

POST image to:

    http://[pi IP address]:10001/

Will return updated map image.

## Tests

    venv\Scripts\activate.bat
    py.test
