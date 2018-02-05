# Flask application
# Create a route called /scrape that will import your scrape_mars.py script and call your  scrape function

# Dependencies
import pymongo
import scrape_mars
from flask import Flask, render_template, redirect

# Create flask app
app = Flask(__name__)

# Connect to MongoDB
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Use database and create it
db = client.marsdataDB
collection = db.marsdata

marsdata = list(db.marsdata.find())
# print(marsdata)

# Create root/index route to query mongoDB and pass mars data to HTML template to display data
@app.route('/')
def index():
    #marsdata = list(db.marsdata.find())
    return render_template('index.html', marsdata=marsdata)

# Create route called /scrape
@app.route('/scrape')
def scrape():
    marsdata = scrape_mars.scrape()
    db.marsdata.update(
        {},
        marsdata,
        upsert=True
    )
    return redirect('http://localhost:5000/', code=302)

if __name__ == '__main__':
    app.run(debug=True)
