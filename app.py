from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

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
    print("GGWEETT host")
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

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)