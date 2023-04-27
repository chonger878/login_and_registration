from flask_app import app
from flask import Flask, render_template
from flask_app.controllers import registrations

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/success')
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)