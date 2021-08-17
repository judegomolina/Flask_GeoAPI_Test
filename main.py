from flask import Flask
from geocoder_blueprint import geocoder_blueprint

app = Flask(__name__)
app.register_blueprint(geocoder_blueprint, url_prefix="")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)