# imports
import csv
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from datetime import date, datetime, timedelta

# create flask app
app = Flask(__name__)

# cors-ify the app
CORS(app)

# variables
residence = ["busch","baker","taylor","smith"]
normal = ["knowlton","recreation","denney","library","enarson"]
types = ["steam","electricity","chilled-water","hot-water","total-consumption","natural-gas"]
start = datetime(2017,1,2) # starting date for all data

# csv openings up here (way more optimized to just open once)

# open dorm csv
with open("./dorm.csv") as dormcsv:
    dormcsv = csv.DictReader(dormcsv)
    dorm_data = list(dormcsv)
# open norm csv
with open("./non-dorm.csv") as normcsv:
    normcsv = csv.DictReader(normcsv)
    norm_data = list(normcsv)

# function to sum all the resouces in a day from the csv
def sumdaily(stamp,building,building_type):
    # difference in days
    diff = stamp - start
    diff = diff.days * 24 # starting row (24 hours in a day)
    
    # if negative do not allow
    if(diff < 0):
        return "BAD STAMP"
    
    # set the file based on type
    if(building_type == "residence"):
        data = dorm_data
    else:
        data = norm_data

    # initialize a dict to store summed values
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
        tmp = data[diff + i] # shift up our data range by current day offset

        # get our different data our of the csv
        steam = tmp[building+" - Steam Consumption (kBTU)"]
        electricity = tmp[building+" - Electricity Consumption (kBTU)"]
        chilled = tmp[building+" - Chilled Water Consumption (kBTU)"]
        hot = tmp[building+" - Hot Water Consumption (kBTU)"]
        total = tmp[building+" - Total Energy Consumption (Cleaned) (kBTU)"]
        natural = tmp[building+" - Natural Gas Consumption (kBTU)"]

        # extremely ugly disgusting chain of if statements for different cases (i could not think of a better way my brain is fried)
        if(steam == "null"):
            pass
        else:
            value = float(steam)
            if value < 0:
                value = 0
            totals["steam"] += value

        if(electricity == "null"):
            pass
        else:
            value = float(electricity)
            if value < 0:
                value = 0
            totals["electricity"] += value

        if(chilled == "null"):
            pass
        else:
            value = float(chilled)
            if value < 0:
                value = 0
            totals["chilled-water"] += value

        if(hot == "null"):
            pass
        else:
            value = float(hot)
            if value < 0:
                value = 0
            totals["hot-water"] += value

        if(total == "null"):
            pass
        else:
            value = float(total)
            if value < 0:
                value = 0
            totals["total-consumption"] += value
        
        if(natural == "null"):
            pass
        else:
            value = float(natural)
            if value < 0:
                value = 0
            totals["natural-gas"] += value

    # return {stamp.strftime("%Y-%m-%d"):totals}
    return totals

# function for getting every day data over an index
def getall(start,days,building,type):
    thing = [] # i am creative at naming variables (but actually though what else would i call this)
    for i in range(days):
        thing.append(sumdaily(datetime(int(start.split("-")[0]),int(start.split("-")[1]),int(start.split("-")[2])) + timedelta(days=i),building,type))
    return thing

@app.route('/api/average/<building>/<stamp>/<rng>')
def weekaverage(building=None,stamp="None",rng=None):
    # standardize parameters for comparing
    building = building.lower()

    # check if the passed building exists
    if building not in residence and building not in normal:
        return "Bad building",400
    else:
        if building in residence:
            type = "residence"
        else:
            type = "normal"

        thing = [] # i am copy pasting shit i give up
        for i in range(int(rng)):
            thing.append( sumdaily( datetime(int(stamp.split("-")[0]),int(stamp.split("-")[1]),int(stamp.split("-")[2])) + timedelta(days= 0-i),building,type ) )

        data = thing
        totals = {
            "steam":0,
            "electricity":0,
            "chilled-water":0,
            "hot-water":0,
            "total-consumption":0,
            "natural-gas":0,
        }
        for day in data:
            for key in day:
                totals[key] += day[key]

        for key in totals:
            totals[key] /= float(rng)

        return jsonify(data) # return this data as a json

# api
# ex: api/busch/2017-01-01/30 (y-m-d)
@app.route('/api/<building>/<stamp>/<range>')
def api(building=None,stamp="None",range=None):
    # standardize parameters for comparing
    building = building.lower()

    # check if the passed building exists
    if building not in residence and building not in normal:
        return "Bad building",400

    # granted our building is valid
    else:
        # data starts jan 2nd 2017
        # if gived X date, it should be sum from ((days since jan 2 2017) * 24) to (((days since jan 2 2017) * 24) + 24) columns
        
        # set building type (used to index specific csv)
        if building in residence:
            type = "residence"
        else:
            type = "normal"

        data = getall(stamp,int(range),building,type) # call the getall method to get data for every single day for this building in this range from a starting date
        return jsonify(data) # return this data as a json

# Path for our main Svelte page
@app.route("/")
def base():
    return "This is an api!" # debug purposes im losing my mind

# run the server on port 5000 locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', use_reloader=True, port=5050)