from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from mltrsc import db, app
from helpers import *


@app.route('/')
def index(prevD):
  return render_template(
    'template.html',
    titulo = 'MLTRSC',
    resultado = prevD
  )

@app.route('/inseriData', methods=['POST', ])
def inseriData():
  data = request.form['data']
  return render_template('template.html', resultado = realizaPrevDia(data, 'n', 'd'))

@app.route('/mes')
def prevMes():
    pass

@app.route('/periodoDias')
def prevPeriodoDias():
    pass

@app.route('/periodoMeses')
def prevPeriodoMeses():
    pass