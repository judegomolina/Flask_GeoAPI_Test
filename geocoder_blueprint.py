from flask import Blueprint, request, abort
import logging
from utilities.utilfunctions import yandex_client, ray_casting, distance_to_polygon

logging.basicConfig(filename='record.log',
                    level=logging.INFO,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

geocoder_blueprint = Blueprint('geocoder_blueprint', __name__)

@geocoder_blueprint.route('/', methods=['POST', 'GET'])
def distance_calculator():
    '''
    This function will receive a post request that should specify an address, and will then return whether or not such an address is inside MKDA, finally, if the address is outside MKDA it computes the distance from the point to it.
    '''
    if request.method == 'POST': # Checking that the url is accessed through a POST request
         # Checking that an address has been specified and it is a string
        if 'address' in request.json and type(request.json['address']) == str:
            address = request.json['address'] # String
            try:
                point = [float(coord) for coord in yandex_client.coordinates(address)] # List of length 2.
                in_polygon = ray_casting(point) # Checking if the point is inside the polygon
                if in_polygon:
                    logging.info(f'{address} is inside MKDA.')
                else:
                    distance = distance_to_polygon(point)
                    logging.info(f'The distance from {address} to MKDA is {distance} km.')
                return 'success', 200
            except:
                logging.critical(f'Yandex Geocoder API did not find address "{address}"')
                abort(400)
        logging.critical('An address was not specified or the format was invalid')
        abort(400) # Aborting due to a Bad Request
    logging.critical('Only POST requests are allowed.')
    abort(400)