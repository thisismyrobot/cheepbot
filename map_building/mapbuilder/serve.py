"""API to the map builder."""
import io

import cv2
import flask
import numpy
import waitress

import mapbuilder.builder as builder


app = flask.Flask(__name__)
the_map = None
the_path = []


@app.route('/')
def test_page():
    return flask.render_template('test.html')


@app.route('/', methods=['POST'])
def step():
    global the_map
    global the_path

    uploaded = flask.request.files['new']
    in_memory_file = io.BytesIO()
    uploaded.save(in_memory_file)
    uploaded.seek(0)
    file_data = in_memory_file.getvalue()
    rotation = builder.read_rotation(file_data)
    data = numpy.fromstring(file_data, dtype=numpy.uint8)
    img = cv2.imdecode(data, 0)

    if the_map is None:
        the_map = img
        the_path = [builder.middle_coordinates(img)]
    else:
        the_path, the_map = builder.step(the_path, the_map, img, rotation)

    map_bytes = cv2.imencode('.jpg', the_map)[1]
    response_stream = io.BytesIO(map_bytes)

    response = flask.make_response(
        flask.send_file(
            response_stream,
            mimetype='image/jpg'
        )
    )
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == '__main__':
    waitress.serve(app, listen='*:10001')
