from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from mltrsc import db, app
from helpers import *

lgb_model_n = treinaML(criaModeloPrevDia('n'))
lgb_model_t = treinaML(criaModeloPrevDia('t'))

@app.route('/')
@app.route('/index')
@app.route('/index/<prev>')
@app.route('/index/<prev><dataInicio><qtdDias>')
def index(titulo='Previsão diária', prev=None, dataInicio=None, qtdDias=None):
  return render_template(
    'template.html',
    titulo=titulo,
    resultado=prev,
    dataInicio=dataInicio,
    qtdDias=qtdDias
  )

@app.route('/realizaPrevD', methods=['POST', ])
def realizaPrevD():
  data = request.form['dataD']
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

@app.route('/realizaPrevP', methods=['POST', ])
def realizaPrevP():
  dataInicio = request.form['dataP']
  dataFim = request.form['dataP']
  tipoTrsc = request.form['tipoTrsc']
  if tipoTrsc == 'n':
    resultado = realizaPrevDia(data, lgb_model_n)
  else:
    resultado = realizaPrevDia(data, lgb_model_t)
  return render_template(
    'template.html', 
    titulo='Previsão de período', 
    resultado=resultado
  )

@app.route('/periodoDias')
def prevPeriodoDias():
    pass

@app.route('/periodoMeses')
def prevPeriodoMeses():
    pass
