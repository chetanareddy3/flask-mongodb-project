import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

# Initialize Flask application
app = Flask(__name__)

# Connect to MongoDB Atlas
mongo_uri = os.environ.get("MONGO_URI")

if not mongo_uri:
    raise RuntimeError("MONGO_URI environment variable is not set")

client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)

# Select database and collection
db = client["beginner_db"]
todos = db["todos"]


# Home page: display all tasks
@app.route("/")
def index():
    all_todos = list(todos.find())
    return render_template("index.html", todos=all_todos)


# Add a new task
@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", "").strip()

    if task:
        todos.insert_one({"task": task})

    return redirect(url_for("index"))


# Run Flask application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
