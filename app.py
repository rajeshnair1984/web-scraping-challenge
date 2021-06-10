from flask import Flask, render_template, redirect
# Import scrape_mars
import scrape_mars
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# Create an instance of our Flask app.
app = Flask(__name__)


# Create connection variable
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


# Set route
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data=destination_data)


# Scrape
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
