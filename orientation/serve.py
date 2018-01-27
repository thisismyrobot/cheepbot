"""RESTful compass reader."""
import flask
import flask_cors
import serial
import waitress


app = flask.Flask(__name__)
flask_cors.CORS(app)


@app.route('/', methods=['GET'])
def get_orientation():
    """Read the magnetic orientation."""
    with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as conn:
        conn.write(bytearray([0x13]))  # 16-bit direction
        dir_bytes = conn.read(2)
        orientation = int.from_bytes(dir_bytes, byteorder='big') / 10
        orientation = (orientation + 180) % 360  # The compass is 180 degrees off when installed.
        return flask.jsonify({'orientation': orientation})


if __name__ == '__main__':
    waitress.serve(app, listen='*:10003')
