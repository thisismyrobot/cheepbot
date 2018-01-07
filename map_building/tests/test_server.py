"""Test of the server's behaviour."""


def test_uploading_two_images_combines_them(webapp):
    """Test of assembling a map."""

    # Given two uploaded files.
    with open('tests/img/1.jpg', 'rb') as img_f:
        response = webapp.post(
            '/map',
            upload_files=[
                ('new', '1.jpg', img_f.read())
            ]
        )

    assert response.status_code == 302
    assert response.headers['location'].endswith('/map')

    with open('tests/img/2.jpg', 'rb') as img_f:
        response = webapp.post(
            '/map',
            upload_files=[
                ('new', '2.jpg', img_f.read())
            ]
        )

    assert response.status_code == 302
    assert response.headers['location'].endswith('/map')

    # When the current map is downloaded
    current = webapp.get('/map')

    # Then it matches the expected image
    with open('tests/img/1+2.png', 'rb') as img_f:
        assert img_f.read() == current.body
