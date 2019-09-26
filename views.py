from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from mltrsc import db, app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dia')
def prevDia():
    pass

@app.route('/mes')
def prevMes():
    pass

@app.route('/periodoDias')
def prevPeriodoDias():
    pass

@app.route('/periodoMeses')
def prevPeriodoMeses():
    pass