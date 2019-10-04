from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from mltrsc import db, app
from helpers import *


@app.route('/')
@app.route('/index')
@app.route('/index/<prev>')
def index(titulo='Previsão diária', prev=0):
  return render_template(
    'template.html',
    titulo=titulo,
    resultado=prev
  )

@app.route('/inseriData', methods=['POST', ])
def inseriData():
  data = request.form['data']
  return render_template('template.html', titulo='Previsão diária', resultado=realizaPrevDia(data, 'n', 'd'))

@app.route('/mes')
def prevMes():
    pass

@app.route('/periodoDias')
def prevPeriodoDias():
    pass

@app.route('/periodoMeses')
def prevPeriodoMeses():
    pass
