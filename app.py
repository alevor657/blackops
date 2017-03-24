#!/usr/bin/env python3
"""
Main module
"""

from flask import Flask, render_template, flash, redirect, url_for, g, request, session
from controller import Controller

app = Flask(__name__, static_folder='lib')

con = Controller()

# Generate a secret word used for sessions
# app.secret_key = os.urandom(24) Does not work on server
app.secret_key = "A very secret key"

@app.before_request
def before_request():
    """
    Runs before all requests
    """
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
            return redirect(url_for('personal'))
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

@app.route('/dashboard/personal/', methods=['GET', 'POST'])
def personal():
    """ Main dashboard """
    if g.user:
        edit_per = request.args.get('edit_per')
        edit_mat = request.args.get('edit_mat')
        workers_backpack = None

        try:
            workers_backpack = con.get_worker(edit_per).backpack.split(', ')
        except AttributeError:
            pass

        if (request.method == 'GET'):
            delete_per = request.args.get('del_per')
            delete_mat = request.args.get('del_mat')

            if (delete_per):
                con.delete_worker(delete_per)
            if (delete_mat):
                con.delete_material(delete_mat)


        if (request.method == 'POST'):
            if 'add_worker' in request.form:
                con.add_worker(request.form)
            elif 'add_material' in request.form:
                con.add_material(request.form)
            elif 'edit_worker' in request.form:
                con.edit_worker(edit_per, request.form)
            elif 'edit_material' in request.form:
                con.edit_material(edit_mat, request.form)


        return render_template(
            'personal.html',
            table_workers=con.create_workers_table(),
            table_material=con.create_material_table(),
            edit_per=edit_per,
            edit_mat=edit_mat,
            worker=con.get_worker(edit_per),
            material=con.get_material(edit_mat),
            av_materials=con.get_avaliable_material(edit_per),
            workers_backpack=workers_backpack
        )
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
    """
    Drops the session
    """

    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
