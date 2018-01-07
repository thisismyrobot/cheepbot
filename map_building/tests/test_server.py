"""Test of the server's behaviour."""
import json


def test_uploading_two_images_combines_them(webapp):
    """Test of assembling a map."""
    given_an_image_is_uploaded(webapp, '1.jpg')
    given_an_image_is_uploaded(webapp, '2.jpg')

    current_map = when_the_map_is_retrieved(webapp)

    # Then it matches the expected image
    with open('tests/img/1+2.png', 'rb') as img_f:
        assert current_map == img_f.read()


def test_uploading_two_images_returns_a_path(webapp):
    """A path is returned during map creation."""
    given_an_image_is_uploaded(webapp, '1.jpg')
    given_an_image_is_uploaded(webapp, '2.jpg')

    current_path = when_the_path_is_retrieved(webapp)

    assert current_path == [[320, 341], [327, 240]]


# Givens

def given_an_image_is_uploaded(webapp, filename):
    with open('tests/img/{}'.format(filename), 'rb') as img_f:
        return webapp.post(
            '/map',
            upload_files=[
                ('new', filename, img_f.read())
            ]
        )


# Whens

def when_the_map_is_retrieved(webapp):
    return webapp.get('/map').body


def when_the_path_is_retrieved(webapp):
    return json.loads(webapp.get('/map').headers['Robot-Path'])
