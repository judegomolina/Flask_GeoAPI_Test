# Flask Geocoder API Task

This test project was dedicated to bulding a simple yet interesting flask app that can receive an address through an HTTP POST request and return whether it is inside Moscow Ring Road (MKDA) or how far it is from it. The application was built with Flask and illustrates a couple of interesting mathematic and geometric concepts in the way it makes its calculations, such as the Ray Casting Algorithm and the Haversian Formula.

The project uses a Flask Blueprint for the main feature in order to make that piece of code as reusable as possible, it also works with Yandex Geocoder API to convert addresses into geocoordinates and includes a set of tests for the code.

## Getting started

The following steps will let you obtain a functional version of this project in your own machine. Please note that if you intend to run this project making use of the predifined Docker container, you just need to have both Docker and Docker-Compose intalled and don't need the rest of this section.

### Installation

In this case no further installation is required besides of cloning this repository with the following piece of code:

> git clone <https://github.com/judegomolina/Flask_GeoAPI_Task>

### Requirements

Requirements are listed under the requirements.txt file which you can use to get all the libraries and packages you need by just running the following command:

> pip3 install -r requirements.txt

However, a list of the required modules is can be found below.

- flask==1.1.2
- colorama==0.4.4
- gunicorn
- yandex-geocoder==2.0.0
- pytest==6.2.4

## Running the project

The way you are going to run this project depends on if you will use the Docker container or not, if you will then you need to run the following command from the command prompt while you are located in the folder:

> docker-compose up --build # if this is the first time you run the container
> or
> docker-compose up # if you have previously built the image

Now, if you are not using docker to run the project you can just run the main.py file from the command prompt or your favorite text editor; however, please take into account that if you want to use this code in a production environment you should configure a WSGI server for the application.

### Making a request

Once the application is up and running you can make a request to it with the following piece of code.

> import requests
> import json
>
> url = 'http://127.0.0.1:80' # Asuming it runs on localhost
>
> data = {'address': 'Caracas, Venezuela'}
>
> r = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
