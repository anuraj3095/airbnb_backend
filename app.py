from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
import csv

app = Flask(__name__)

def get_db():
    client = MongoClient(host='airbnb_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client['airbnb_db']
    return db

@app.route('/')
def ping_server():
    return "Server is working."

@app.route('/hostings')
def get_hostings():
    print("GET host")
    db=""
    try:
        db = get_db()
        print("got the db")
        col = db["airbnb_hostings"]
        #print(col)
        hostings = col.find()
        hl = []
        for h in hostings:
            del h['_id']
            print(h)
            hl.append(h)
        print(hl)
        return jsonify({"hostings": hl})
    except:
        pass
    finally:
        if type(db)==MongoClient:
            print("closing db")
            db.close()
    return  jsonify({  "brand": "Ford" })

@app.route('/load')
def load_database():
    db=""
    try:
        db = get_db()
        print("got the db")
        airbnb_col = db["airbnb_hostings"]
        count = airbnb_col.count()
        print(count)
        if count > 0 :
            return "Collection conatins data...skipping loading"

        with open('listings_10.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rowDict = dict(row)
                print(rowDict)
                name = rowDict['name']
                price = rowDict['price']
                airbnb_col.insert({'name': name, 'price': price})
        new_hostings = airbnb_col.find()
        hl = []
        for h in new_hostings:
            del h['_id']
            print(h)
            hl.append(h)
        print(hl)
        return jsonify({"hostings": hl})
    except:
        pass
    finally:
        if type(db)==MongoClient:
            print("closing db")
            db.close()
    return "Error loading data into database..."

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)