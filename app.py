#!/usr/bin/env python3

from flask import Flask, render_template, flash, redirect, url_for, g, request, session
from controller import Controller

app = Flask(__name__)
con = Controller()

# Generate a secret word used for sessions
# app.secret_key = os.urandom(24) Does not work on server
app.secret_key = "A very secret key"

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Login page """
    if request.method == 'POST':

        session['user'] = con.check_login_data(request.form)
        g.user = session['user']
        if g.user:
            return redirect(url_for('dashboard'))
        else:
            flash("Bad password, try again")
            return redirect(url_for('index'))
    else:
        return render_template('index.html')


@app.route('/dashboard/')
def dashboard():
    """ Main dashboard """
    if g.user:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/dashboard/personal/', methods=['GET'])
def personal():
    """ Main dashboard """
    if g.user:
        return render_template('personal.html', table=con.create_workers_table())
    else:
        return redirect(url_for('index'))

@app.route('/dashboard/material')
def material():
    """ Main dashboard """
    if g.user:
        return render_template('material.html')
    else:
        return redirect(url_for('index'))

@app.route('/dropsession/')
def dropsession():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
