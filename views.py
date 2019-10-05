from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from mltrsc import db, app
from helpers import *

lgb_model_n = treinaML(criaModeloPrevDia('n'))
lgb_model_t = treinaML(criaModeloPrevDia('t'))

@app.route('/')
@app.route('/index')
@app.route('/index/<prev>')
def index(titulo='Previsão diária', prev=0):
  return render_template(
    'template.html',
    titulo=titulo,
    resultado=prev
  )

@app.route('/realizaPrev', methods=['POST', ])
def realizaPrev():
  data = request.form['data']
  tipoTrsc = request.form['tipoTrsc']
  if tipoTrsc == 'n':
    resultado = realizaPrevDia(data, lgb_model_n)
  else:
    resultado = realizaPrevDia(data, lgb_model_t)
  return render_template(
    'template.html', 
    titulo='Previsão diária', 
    resultado=resultado
  )

@app.route('/mes')
def prevMes():
    pass

@app.route('/periodoDias')
def prevPeriodoDias():
    pass

@app.route('/periodoMeses')
def prevPeriodoMeses():
    pass
