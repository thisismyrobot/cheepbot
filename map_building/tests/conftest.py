import pytest
import flask_webtest

import mapbuilder.serve


@pytest.fixture
def webapp():
    """Create a webapp fixture for accessing the site.

    Just include 'webapp' as an argument to the test method to use.
    """
    # Create a webtest Test App for use
    testapp = flask_webtest.TestApp(mapbuilder.serve.app)
    testapp.app.debug = True

    # Make sure there's no map.
    testapp.delete('/map')

    return testapp
