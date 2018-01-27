"""Command centre to drive it all."""
import flask
import waitress


app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template('index.html')


if __name__ == '__main__':
    waitress.serve(app, listen='*:9999')
