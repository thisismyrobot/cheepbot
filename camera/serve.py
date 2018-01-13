"""Return images from a Pi camera over HTTP."""
import io

import flask
import picamera
import piexif
import waitress


app = flask.Flask(__name__)
camera = None


def add_rotation(img_stream):
    """Add rotation information to the exif data."""
    rotation = 0  # Until we get a sensor...
    gps_tags = {
        piexif.GPSIFD.GPSImgDirectionRef: 'M',
        piexif.GPSIFD.GPSImgDirection: (rotation, 100),
    }
    exif_bytes = piexif.dump({'GPS': gps_tags})
    updated_stream = io.BytesIO()
    piexif.insert(exif_bytes, img_stream.getvalue(), updated_stream)
    return updated_stream


@app.route('/')
def photo():
    stream = io.BytesIO()
    camera.capture(stream, 'jpeg')
    stream = add_rotation(stream)
    stream.seek(0)
    return flask.send_file(stream, mimetype='image/jpg')


if __name__ == '__main__':
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    waitress.serve(app, listen='*:10000')
