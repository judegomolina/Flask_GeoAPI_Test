import pytest
from flask import Flask
from geocoder_blueprint import geocoder_blueprint
from utilities.utilfunctions import ray_casting, distance_to_polygon
from utilities.ref_data import mkad_perimeter


# Unit tests for utilitary functions

@pytest.mark.parametrize(
    'point, polygon, result',
    [
        # Caracas, Venezuela
        ([-66.919512, 10.503556], mkad_perimeter, False),
        # Madrid, Spain
        ([-3.703978, 40.416766], mkad_perimeter, False),
        # Moscow, Russia
        ([37.622513, 55.75322], mkad_perimeter, True),
        # Boston, USA
        ([-71.065489, 42.354371], mkad_perimeter, False),
        # London, UK
        ([-0.127696, 51.507351], mkad_perimeter, False)
    ]
)
def test_ray_casting(point, polygon, result):
    assert ray_casting(point, polygon) == result

@pytest.mark.parametrize(
    'point, polygon, result',
    [
        # Caracas, Venezuela
        ([-66.919512, 10.503556], mkad_perimeter, 9927),
        # Madrid, Spain
        ([-3.703978, 40.416766], mkad_perimeter, 4110),
        # Boston, USA
        ([-71.065489, 42.354371], mkad_perimeter, 7215),
        # London, UK
        ([-0.127696, 51.507351], mkad_perimeter, 2880)
    ]
)
def test_distance_to_polygon(point, polygon, result):
    '''In this test we compare the value outputed by the function to the distanced reported by Google from the start point to the center of Moscow, therefore we add 20% of tolerance to account for both the distance from the center of the city to the MKDA and slight unaccuracies related to the implemented algorithm.'''
    assert 1.2 * result > distance_to_polygon(point, polygon) > 0.8 * result


# Functional testS

def test_blueprint_get():
    '''
    GIVEN a Flask app identical to the one we use in production
    WHEN the "/" page is requested (GET)
    THEN check that response code is 400
    '''

    # First we create a test app
    test_app = Flask(__name__)
    test_app.register_blueprint(geocoder_blueprint, url_prefix="")

    # Then we create a test client using the test Flask app
    with test_app.test_client() as test_client:
        response = test_client.get('/')
        # Finally we check that the response code is 400, meaning that the app is not accesible through POST method
        assert response.status_code == 400

@pytest.mark.parametrize(
    'json, response_code',
    [
        # Successful request
        ({'address': 'Madrid, Spain'}, 200),
        # Unnecessary arguments but still a successful request
        ({'address': 'Lima, Peru', 'color': 'red'}, 200),
        # Not address in the json
        ({'color': 'red'}, 400),
        # Not a valid address
        ({'address': 'non-existing address'}, 400),
        # unexpected data type
        ({'address': [154654654]}, 400)
    ]
)
def test_blueprint_post(json, response_code):
    '''
    GIVEN a Flask app identical to the one we use in production
    WHEN the "/" page is requested (GET)
    THEN check that response code is the expected depending on the case
    '''

    # First we create a test app
    test_app = Flask(__name__)
    test_app.register_blueprint(geocoder_blueprint, url_prefix="")

    # Then we create a test client using the test Flask app
    with test_app.test_client() as test_client:
        response = test_client.post('/', json=json)
        # Finally we check that the response code is the one we expected
        assert response.status_code == response_code