# imports
import csv
from distutils.command.build import build
from flask import Flask
from flask_cors import CORS
from datetime import datetime

# create flask app
app = Flask(__name__)

# cors-ify the app
CORS(app)

# variables
residence = ["busch","baker","taylor","smith"]
normal = ["knowlton","recreation","denney","library","enarson"]
types = ["steam","electricity","chilled-water","hot-water","total-consumption","natural-gas"]
start = datetime(2017,1,2) # starting date for all data

# optimization shit
dorm_file = open("./dorm.csv", 'r')
non_dorm_file = open("./non-dorm.csv", 'r')


# normal functions

# sum all the resouces in a day from the csv
def sumdaily(stamp,building,building_type):
    # difference in days
    diff = stamp - start
    diff = diff.days * 24 # starting row
    
    # if negative do not allow
    if(diff < 0):
        return "BAD STAMP"
    
    # set the file based on type
    if(building_type == "residence"):
        tmp = dorm_file
    else:
        tmp = non_dorm_file
    
    # open csv
    f = csv.DictReader(tmp)
    data = list(f)

    totals = {
        "steam":0,
        "electricity":0,
        "chilled-water":0,
        "hot-water":0,
        "total-consumption":0,
        "natural-gas":0,
    }

    # for loop that iterates through data[diff] to data[diff] + 24 and totals in a list the different consumptions
    for i in range(24):
        tmp = data[diff + i]
        print(diff,i,len(data))

        steam = tmp[building+" - Steam Consumption (kBTU)"]
        electricity = tmp[building+" - Electricity Consumption (kBTU)"]
        chilled = tmp[building+" - Chilled Water Consumption (kBTU)"]
        hot = tmp[building+" - Hot Water Consumption (kBTU)"]
        total = tmp[building+" - Total Energy Consumption (Cleaned) (kBTU)"]
        natural = tmp[building+" - Natural Gas Consumption (kBTU)"]

        if(steam == "null"):
            pass
        else:
            totals["steam"] += float(steam)

        if(electricity == "null"):
            pass
        else:
            totals["electricity"] += float(electricity)

        if(chilled == "null"):
            pass
        else:
            totals["chilled-water"] += float(chilled)

        if(hot == "null"):
            pass
        else:
            totals["hot-water"] += float(hot)

        if(total == "null"):
            pass
        else:
            totals["total-consumption"] += float(total)
        
        if(natural == "null"):
            pass
        else:
            totals["natural-gas"] += float(natural)

    return totals

# function for getting every day data over an index
def getall(start,days,building,type):
    thing = []
    for i in range(days):
        thing.append(sumdaily(datetime(int(start.split("-")[0]),int(start.split("-")[1]),int(start.split("-")[2])),building,type))
    return thing

# api
# ex: api/busch/steam/2017-01-01/30 (y-m-d)
@app.route('/api/<building>/<stamp>/<range>')
def api(building=None,stamp="None",range=None):
    # standardize parameters for comparing
    building = building.lower()

    # check if the passed building exists
    if building not in residence and building not in normal:
        return "Bad building",400
    # granted our types and buildings are valid
    else:
        # data starts jan 2nd 2017
        # if gived X date, it should be sum from ((days since jan 2 2017) * 24) to (((days since jan 2 2017) * 24) + 24) columns
        
        # set building type (used to index specific csv)
        if building in residence:
            type = "residence"
        else:
            type = "normal"

        
        # date = parser.parse("2017-01-01T12:00:00")
        stamp = getall(stamp,int(range),building,type)
        return str(stamp)

# run the server on port 5000 locally
if __name__ == '__main__':
    app.run(host='127.0.0.1', use_reloader=True, port=5000, threaded=True, debug=True)