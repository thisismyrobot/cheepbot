"""RESTful motor driver."""
import flask
import serial
import waitress

import commands


app = flask.Flask(__name__)


COMMANDS = (
    'forward',
    'stop'
)


@app.route('/motor', methods=['GET'])
def test_page():
    return flask.render_template('test.html')


@app.route('/motor/command', methods=['POST'])
def take_command():
    """Responds to POSTed motor commands."""
    command = flask.request.form['command']
    if command not in COMMANDS:
        flask.abort(400) 

    command_bytes = getattr(commands, command)()

    with serial.Serial('/dev/ttyS0', 38400, timeout=1) as conn:
        conn.write(command_bytes)

    return ('', 200)


if __name__ == '__main__':
    waitress.serve(app, listen='*:10002')
