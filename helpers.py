import pandas as pd
import numpy as np
from datetime import date, datetime, timezone
from sklearn.model_selection import train_test_split
from sklearn import metrics
from lightgbm import LGBMRegressor

from workalendar.america import Brazil
cal = Brazil()

def obterFeriados(inicio, fim):
    qtdAnos = (fim - inicio) + 1
    frds = []

    for i in range(qtdAnos):
        frds.append([d[0] for d in cal.holidays(inicio+i)])
    frds = np.asarray(frds)
    frds = frds.reshape(1, frds.size)
    feriados = pd.DataFrame({'data': frds[0]})
    feriados.data = pd.to_datetime(feriados.data)

    return feriados

def criaModeloPrevDia(nomeArqv):
    dfDia = pd.read_csv(f'./files/{nomeArqv}.csv', sep=';', index_col=0)

    dfDia['data'] = pd.to_datetime(dfDia['data'], format='%Y-%m-%d')
    anoMin = dfDia['data'].min().year
    anoMax = dfDia['data'].max().year
    tmp = pd.merge(dfDia.data, obterFeriados(anoMin, anoMax).data, how='left', on='data', indicator=True)
    dfDia['feriado'] = np.where(tmp['_merge'] == 'both', 1, 0)
    dfDia['dia'] = (dfDia['data'].dt.day)
    dfDia['mes'] = (dfDia['data'].dt.month)
    dfDia['ano'] = (dfDia['data'].dt.year)
    dfDia['diaAno'] = (dfDia['data'].dt.dayofyear)
    dfDia['diaSemana'] = (dfDia['data'].dt.dayofweek)
    dfDia['numSemanaMes'] = ((dfDia['dia'] - 1) // 7 + 1)
    dfDia['diaUtil'] = ((dfDia['diaSemana'] < 5) & (dfDia['feriado'] == 0))
    dfDia['diaDeProducao'] = (((dfDia['diaSemana'] == 1) | (dfDia['diaSemana'] == 3)) & dfDia['diaUtil'] == True)
    dfDia['dia5'] = 0
    dfDia['dia10'] = 0

    meses = np.array(dfDia['mes'])
    anos = np.array(dfDia['ano'])

    for i in range(len(dfDia)):
        if (dfDia.iloc[i, 1] == pd.Timestamp(cal.add_working_days(date(anos[i], meses[i], 1), 5))):
            dfDia['dia5'][i] = 1
        if (dfDia.iloc[i, 1] == pd.Timestamp(cal.add_working_days(date(anos[i], meses[i], 1), 10))):
            dfDia['dia10'][i] = 1

    dfDia['segDia5'] = ((dfDia['data'].dt.dayofweek == 0) & (dfDia['dia'] == 5) & (dfDia['feriado'] == 0))
    dfDia['segDia10'] = ((dfDia['data'].dt.dayofweek == 0) & (dfDia['dia'] == 10) & (dfDia['feriado'] == 0))
    dfDia['inicioSemana'] = (dfDia['diaSemana'] < 3)
    dfDia['semanaAno'] = (dfDia['data'].dt.weekofyear)
    dfDia['inicioMes'] = (dfDia['data'].dt.is_month_start)
    dfDia['fimMes'] = (dfDia['data'].dt.is_month_end)

    trocar = {True: 1, False: 0}

    dfDia['diaUtil'] = dfDia['diaUtil'].map(trocar)
    dfDia['inicioMes'] = dfDia['inicioMes'].map(trocar)
    dfDia['fimMes'] = dfDia['fimMes'].map(trocar)
    dfDia['inicioSemana'] = dfDia['inicioSemana'].map(trocar)
    dfDia['segDia5'] = dfDia['segDia5'].map(trocar)
    dfDia['segDia10'] = dfDia['segDia10'].map(trocar)
    dfDia['diaDeProducao'] = dfDia['diaDeProducao'].map(trocar)

    return dfDia

def criaModeloPrevMes(nomeArqv):
    dfMes = pd.read_csv(f'./files/{nomeArqv}.csv', sep=';', index_col=0)
    dfMes['data'] = pd.to_datetime(dfMes['data'], format('%d/%m/%Y'))

    return dfMes

def treinaML(df):
    x = df[['feriado', 'dia', 'mes', 'ano', 'diaAno', 'diaSemana', 'numSemanaMes', 'diaUtil', 'segDia5', 'segDia10', 'diaDeProducao', 'dia5', 'dia10', 'inicioSemana', 'semanaAno', 'inicioMes', 'fimMes']]
    y = df['qtd']

    SEED = 5
    np.random.seed(SEED)
    x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.33, random_state=SEED)
    print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(x_treino), len(x_teste)))

    lgb_model = LGBMRegressor()
    lgb_model.fit(x_treino, y_treino)
    print('R² = {}'.format(lgb_model.score(x_treino, y_treino).round(3)))
    y_previsto = lgb_model.predict(x_teste)
    print('R² = %s' % metrics.r2_score(y_teste, y_previsto).round(3))

    return lgb_model

def realizaPrevDia(data):
    data = pd.to_datetime(data, format='%Y-%m-%d')

    if(data == cal.is_holiday(data.dt.year)):


def realizaPrevMes():
    pass

def realizaPrevPeriodoDiario():
    pass

def realizaPrevPeriodoMensal():
    pass