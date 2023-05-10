from flask import Flask, Blueprint, render_template, redirect, url_for, request
from werkzeug.middleware.proxy_fix import ProxyFix
import sys
from argparse import ArgumentParser
from cvd_model import *

appweb = Blueprint('hello', __name__)

@appweb.route('/')
def home():
    return render_template("index.html")

@appweb.route('/send', methods=['POST'])
def send(predict=predict):
    if request.method == 'POST':
        car_model = request.form['model']
        car_date = request.form['date']
        car_fuel = request.form['fuel']
        car_mileage = request.form['mileage']
        car_swift = request.form['swift']
        car_price = request.form['price']
        car_hp = request.form['hp']
        trainmodel = request.form['trainmodel']

        date_value = car_date
        timestamp_value = pd.Timestamp(date_value)
        car_date = timestamp_value.value // 10 ** 9

        if(car_fuel == "diesel"):
            car_fuel = 0
        elif(car_fuel == "gpl"):
            car_fuel = 1
        else:
            car_fuel = 2

        if (car_swift == "Automatic"):
            car_swift = 0
        else:
            car_swift = 1

        if (trainmodel == "default"):
            trainmodel = best_model
        elif (trainmodel == "dt"):
            trainmodel = dt
        elif (trainmodel == "gnb"):
            trainmodel = nb
        elif (trainmodel == "svc"):
            trainmodel = svc
        elif (trainmodel == "gbc"):
            trainmodel = gb
        else:
            trainmodel = rf

        # Accuracy of Model
        trainmodel.fit(x_train, y_train) #<-- this line
        acc = trainmodel.score(x_train, y_train)

        predict_real = trainmodel.predict([[car_model,car_date,car_fuel,car_mileage,car_swift,car_price,car_hp]])

        if(predict_real == [0]):
            predict = "The result returned with " + str(round(acc,5)*100)  + "% accuracy and car have a higher chance of Dealer"
        else:
            predict = "The result returned with " + str(round(acc,5)*100) + "% accuracy and car have a higher chance of Private"


        return render_template('index.html', predict=predict)

    else:
        return render_template('index.html', predict=predict)



@appweb.route('/about')
def about():
    return render_template("about.html")



if __name__ == '__main__':

    # arg parser for the standard anaconda-project options
    parser = ArgumentParser(prog="home",
                            description="Simple Flask Application")
    parser.add_argument('--anaconda-project-host', action='append', default=[],
                        help='Hostname to allow in requests')
    parser.add_argument('--anaconda-project-port', action='store', default=8086, type=int,
                        help='Port to listen on')
    parser.add_argument('--anaconda-project-iframe-hosts',
                        action='append',
                        help='Space-separated hosts which can embed us in an iframe per our Content-Security-Policy')
    parser.add_argument('--anaconda-project-no-browser', action='store_true',
                        default=False,
                        help='Disable opening in a browser')
    parser.add_argument('--anaconda-project-use-xheaders',
                        action='store_true',
                        default=False,
                        help='Trust X-headers from reverse proxy')
    parser.add_argument('--anaconda-project-url-prefix', action='store', default='',
                        help='Prefix in front of urls')
    parser.add_argument('--anaconda-project-address',
                        action='store',
                        #default='0.0.0.0',
                        help='IP address the application should listen on.')

    args = parser.parse_args()

    app = Flask(__name__)
    app.register_blueprint(appweb, url_prefix = args.anaconda_project_url_prefix)

    app.config['PREFERRED_URL_SCHEME'] = 'https'

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host=args.anaconda_project_address, port=args.anaconda_project_port)
