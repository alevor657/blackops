#!/usr/bin/env python3

from flask import Flask, render_template, flash

app = Flask(__name__)

# Generate a secret word used for sessions
# app.secret_key = os.urandom(24) Does not work on server
app.secret_key = "A very secret key"

@app.route('/')
def index():
    """ Login page """
    flash("Bad password, try again")
    # flash("P.S. admin/admin")
    return render_template('index.html')

@app.route('/dashboard/')
def dashboard():
    """ Main dashboard """
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
