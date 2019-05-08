from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    latest_data = mongo.db.collection.find_one()

    # Return template and data
    return( render_template("index.html", latest_info=latest_data) )

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)
    
    mongo.db.history_record.insert_one(mars_data)

    # Redirect back to home page
    return( redirect("/") )

if __name__ == "__main__":
    app.run(debug=True)