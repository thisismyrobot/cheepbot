"""Return images from a Pi camera over HTTP."""
import io

import flask
import picamera
import waitress


app = flask.Flask(__name__)
camera = None


@app.route('/')
def photo():
    stream = io.BytesIO()
    camera.capture(stream, 'jpeg')
    stream.seek(0)
    return flask.send_file(stream, mimetype='image/jpg')


if __name__ == '__main__':
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    waitress.serve(app, listen='*:10000')
