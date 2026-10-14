from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

# Initialize the Flask application
app = Flask(__name__)

# Connect to the local MongoDB instance
client = MongoClient("mongodb://localhost:27017/")

# Select the database and collection
db = client["beginner_db"]
todos = db["todos"]


@app.route("/")
def index():
    # Retrieve all documents from the todos collection
    all_todos = list(todos.find())
    return render_template("index.html", todos=all_todos)


@app.route("/add", methods=["POST"])
def add():
    # Read the submitted form field named 'task'
    task = request.form.get("task")
    # Only insert if the task is not empty
    if task:
        todos.insert_one({"task": task})
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
