import pandas as pd
import numpy as np
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn import metrics
from lightgbm import LGBMRegressor

from workalendar.america import Brazil
cal = Brazil()

def obterFeriadosAuto(inicio, fim):
    qtdAnos = (fim - inicio) + 1
    frds = []

    for i in range(qtdAnos):
        frds.append([d[0] for d in cal.holidays(inicio+i)])
    frds = np.asarray(frds)
    frds = frds.reshape(1, frds.size)
    feriados = pd.DataFrame({'data': frds[0]})
    feriados.data = pd.to_datetime(feriados.data)

    return feriados

def obterFeriadosManual():
    feriados = [
        '2015-01-01','2015-02-17','2015-04-03','2015-04-05','2015-04-21','2015-05-01','2015-06-04','2015-09-07','2015-10-12','2015-11-02','2015-11-15','2015-12-25',
        '2016-01-01','2016-02-09','2016-03-25','2016-03-27','2016-04-21','2016-05-01','2016-05-26','2016-06-04','2016-09-07','2016-10-12','2016-11-02','2016-11-15','2016-12-25',
        '2017-01-01','2017-02-28','2017-04-14','2017-04-16','2017-04-21','2017-05-01','2017-05-26','2017-06-15','2017-09-07','2017-10-12','2017-11-02','2017-11-15','2017-12-25',
        '2018-01-01','2018-02-13','2018-03-30','2018-04-01','2018-04-21','2018-05-01', '2018-05-31','2018-09-07','2018-10-12','2018-11-02','2018-11-15','2018-12-25',
        '2019-01-01', '2019-03-05','2019-04-19', '2019-04-21','2019-05-01','2019-06-20','2019-09-07','2019-10-12','2019-11-02','2019-11-15','2019-12-25'
    ]
    feriados = pd.to_datetime(feriados, format='%Y-%m-%d')
    feriados = pd.DataFrame({'data': feriados})
    return feriados

def criaModeloPrevDia(tipoTrsc):
    
    tipoTrsc.lower()
    if tipoTrsc == 'n':
        dfDia = pd.read_csv('Z:\\mltrsc\\files\\qtdTrscNgc_Diario.csv', sep=';', index_col=0)
    elif tipoTrsc == 't':
        dfDia = pd.read_csv('Z:\\mltrsc\\files\\qtdTrsc_Diario.csv', sep=';', index_col=0)
    else:
        return None

    dfDia['data'] = pd.to_datetime(dfDia['data'], format='%Y-%m-%d')
    anoMin = dfDia['data'].min().year
    anoMax = dfDia['data'].max().year
    #tmp = pd.merge(dfDia.data, obterFeriadosManual().data, how='left', on='data', indicator=True)
    tmp = pd.merge(dfDia.data, obterFeriadosAuto(anoMin, anoMax).data, how='left', on='data', indicator=True)
    dfDia['feriado'] = np.where(tmp['_merge'] == 'both', 1, 0)
    dfDia['dia'] = (dfDia['data'].dt.day)
    dfDia['mes'] = (dfDia['data'].dt.month)
    dfDia['ano'] = (dfDia['data'].dt.year)
    dfDia['diaAno'] = (dfDia['data'].dt.dayofyear)
    dfDia['diaSemana'] = (dfDia['data'].dt.dayofweek)
    dfDia['numSemanaMes'] = ((dfDia['dia'] - 1) // 7 + 1)
    dfDia['diaUtil'] = ((dfDia['diaSemana'] < 5) & (dfDia['feriado'] == 0))
    dfDia['diaDeProducao'] = (((dfDia['diaSemana'] == 1) | (dfDia['diaSemana'] == 3)) & dfDia['diaUtil'] == True)
    dfDia['seg'] = dfDia['diaSemana'] == 0
    dfDia['dia5'] = 0
    dfDia['dia10'] = 0
    dfDia['dia11'] = 0
    dfDia['dia12'] = 0
    dfDia['diaUtil5'] = 0
    dfDia['diaUtil10'] = 0

    meses = np.array(dfDia['mes'].tolist())
    anos = np.array(dfDia['ano'].tolist())

    for i in range(len(dfDia)):
        if dfDia.iloc[i, 0] == pd.Timestamp(cal.add_working_days(date(anos[i], meses[i], 1), 5)):
            dfDia.iloc[i, 16] = 1
        if dfDia.iloc[i, 0] == pd.Timestamp(cal.add_working_days(date(anos[i], meses[i], 1), 10)):
            dfDia.iloc[i, 17] = 1
        if dfDia.iloc[i, 3] == 5:
            if dfDia.iloc[i, 1] == 1 & dfDia.iloc[i+1, 7] == 5:
                dfDia.iloc[i+3, 12] = 1
            elif dfDia.iloc[i, 1] == 1 & dfDia.iloc[i+1, 7] == 0:
                dfDia.iloc[i+1, 12] = 1
            elif dfDia.iloc[i, 1] == 0:
                dfDia.iloc[i, 12] = 1
            elif dfDia.iloc[i, 7] == 5:
                dfDia.iloc[i+2, 12] = 1
            elif dfDia.iloc[i, 7] == 6:
                dfDia.iloc[i+1, 12] = 1
        if dfDia.iloc[i, 3] == 10:
            if dfDia.iloc[i, 1] == 1 & dfDia.iloc[i+1, 7] == 5:
                dfDia.iloc[i+3, 13] = 1
                dfDia.iloc[i+3, 14] = 1
                dfDia.iloc[i+3, 15] = 1
            elif dfDia.iloc[i, 1] == 1 & dfDia.iloc[i+1, 7] == 0:
                dfDia.iloc[i+1, 13] = 1
                dfDia.iloc[i+1, 14] = 1
                dfDia.iloc[i+1, 15] = 1
            elif dfDia.iloc[i, 1] == 0:
                dfDia.iloc[i, 13] = 1
                dfDia.iloc[i, 14] = 1
                dfDia.iloc[i, 15] = 1
            elif dfDia.iloc[i, 7] == 5:
                dfDia.iloc[i+2, 13] = 1
                dfDia.iloc[i+2, 14] = 1
                dfDia.iloc[i+2, 15] = 1
            elif dfDia.iloc[i, 7] == 6:
                dfDia.iloc[i+1, 13] = 1
                dfDia.iloc[i+1, 14] = 1
                dfDia.iloc[i+1, 15] = 1

    dfDia['segDia5'] = ((dfDia['data'].dt.dayofweek == 0) & (dfDia['dia'] == 5) & (dfDia['feriado'] == 0))
    dfDia['segDia10'] = ((dfDia['data'].dt.dayofweek == 0) & (dfDia['dia'] == 10) & (dfDia['feriado'] == 0))
    dfDia['inicioSemana'] = (dfDia['diaSemana'] < 3)
    dfDia['semanaAno'] = dfDia['data'].dt.weekofyear
    dfDia['inicioMes'] = (dfDia['dia'] < 15)

    trocar = {True: 1, False: 0}
    dfDia['diaUtil'] = dfDia['diaUtil'].map(trocar)
    dfDia['inicioMes'] = dfDia['inicioMes'].map(trocar)
    #dfDia['fimMes'] = dfDia['fimMes'].map(trocar)
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
    x = df[['feriado', 'dia', 'mes', 'ano', 'diaAno', 'diaSemana', 'diaUtil', 'segDia5', 'segDia10','diaDeProducao','seg', 'diaUtil5', 'diaUtil10', 'inicioSemana', 'semanaAno', 'inicioMes']]
    y = df['qtd']

    SEED = 5
    np.random.seed(SEED)
    x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size=0.30, random_state=SEED)
    print("Treinaremos com %d elementos e testaremos com %d elementos" % (len(x_treino), len(x_teste)))

    lgb_model = LGBMRegressor()
    lgb_model.fit(x_treino, y_treino)
    print('R² = {}'.format(lgb_model.score(x_treino, y_treino).round(3)))
    y_previsto = lgb_model.predict(x_teste)
    print('R² = %s' % metrics.r2_score(y_teste, y_previsto).round(3))

    return lgb_model

def realizaPrevDia(data, lgb_model):

    data = pd.to_datetime(data, format='%Y-%m-%d')

    entrd = []
    frds = obterFeriadosAuto(data.year, data.year)

    for i in range(len(frds)):
        if frds.data[i] == data:
            entrd.append(1)#Feriado
        else:
            entrd.append(0)#Feriado
        break
    entrd.append(data.day)#Dia
    entrd.append(data.month)#Mes
    entrd.append(data.year)#Ano
    entrd.append(data.dayofyear)#Dia do ano
    entrd.append(data.dayofweek)#Dia da semana
    #entrd.append(((data.day - 1) // 7 + 1))#Semana do mes
    if (data.dayofweek < 5) & (entrd[0] == 0):
        entrd.append(1)#Dia util
    else:
        entrd.append(0)#Dia util
    if ((data.dayofweek == 1) | (data.dayofweek == 3)) & (entrd[0] == 0):
        entrd.append(1)#Dia de Produção
    else:
        entrd.append(0)#Dia de Produção
    if data.dayofweek == 0:
        entrd.append(1)#Seg
    else:
        entrd.append(0)#Seg
    if data == pd.Timestamp(cal.add_working_days(date(data.year, data.month, 1), 5)):
       entrd.append(1)#DiaUtil5
    else:
        entrd.append(0)#DiaUtil5
    if data == pd.Timestamp(cal.add_working_days(date(data.year, data.month, 1), 10)):
        entrd.append(1)#DiaUtil10
    else:
        entrd.append(0)#DiaUtil10
    if (data.dayofweek == 0 & data.day == 5) & (entrd[0] == 0):
        entrd.append(1)#Segunda dia 5
    else:
        entrd.append(0)#Segunda dia 5
    if (data.dayofweek == 0 & data.day == 10) & (entrd[0] == 0):
        entrd.append(1)#Segunda dia 10
    else:
        entrd.append(0)#Segunda dia 10
    if data.dayofweek < 3:
        entrd.append(1)#Inicio da semana
    else:
        entrd.append(0)#Inicio da semana
    entrd.append(data.weekofyear)#Semana do ano
    if data.day < 15:
        entrd.append(1)#Inicio do mes
    else:
        entrd.append(0)#Inicio do mes

    prev = int(lgb_model.predict(np.array([entrd])))
    print('Dia: {:02d} LGBR: {}'.format(data.day, prev))
    return prev

def realizaPrevMes():
    pass

def realizaPrevPeriodoDiario(dataInicio, qtdDias, lgb_model):
    pass


def realizaPrevPeriodoMensal():
    pass

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)