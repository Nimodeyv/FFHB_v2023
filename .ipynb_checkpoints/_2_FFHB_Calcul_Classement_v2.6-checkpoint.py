import sqlite3
from collections import defaultdict
import pandas as pd
import time
#import matplotlib.pyplot as plt
#from sklearn.linear_model import LinearRegression
#import numpy as np
#from datetime import date
#
start = time.time() # To measure time

conn = sqlite3.connect('Championnat_U18_GrandEst.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Matchs')
rows = cur.fetchall()
Matchs =list()
for row in rows:
    m = dict()
    m['fichier']=row[0]
    m['Journee']=row[1]
    m['Periode']=row[2]
    m['Date']=row[3]
    m['equipe_dom']=row[4]
    m['equipe_ext']=row[5]
    m['score_dom']=row[6]
    m['score_ext']=row[7]
    m['diff_buts']=row[8]
    m['lieu']=row[9]
    m['arbitres']=row[10]
    Matchs.append(m)
#print(Matchs)
print('Nombre de matchs au total dans le championnat:',len(Matchs))

# DEFINITION DE LA LISTE DES EQUIPE
Liste_equipe = []
for m in Matchs:
    if m['equipe_dom'] not in Liste_equipe : Liste_equipe.append(m['equipe_dom'])
    if m['equipe_ext'] not in Liste_equipe : Liste_equipe.append(m['equipe_ext'])
print('Nombre d"equipes dans le championnat:',len(Liste_equipe))

# CALCUL DU CLASSEMENT
classement = defaultdict(dict)
col = ['PTS','G','N','P','Buts+','Buts-','Diff','J_dom','J_ext']
for eq in Liste_equipe:
    classement[eq]=defaultdict(int)
    for c in col:
        classement[eq][c]=0
for m in Matchs[:]: # To consider only a number of match ADD Match[:XX] instead of Matchs[:]
    if m['score_dom']!='':
        classement[m['equipe_dom']]['J_dom']+=1
        classement[m['equipe_ext']]['J_ext']+=1
        if m['score_dom']==-1: # si forfait pour dom
            classement[m['equipe_dom']]['P']+=1
            classement[m['equipe_dom']]['PTS']+=0
            classement[m['equipe_ext']]['G']+=1
            classement[m['equipe_ext']]['PTS']+=3
        elif m['score_ext']==-1: # si forfait pour ext
            classement[m['equipe_dom']]['G']+=1
            classement[m['equipe_dom']]['PTS']+=3
            classement[m['equipe_ext']]['P']+=1
            classement[m['equipe_ext']]['PTS']+=0
        elif m['score_dom']>m['score_ext'] :
            classement[m['equipe_dom']]['G']+=1
            classement[m['equipe_dom']]['PTS']+=3
            classement[m['equipe_ext']]['P']+=1
            classement[m['equipe_ext']]['PTS']+=1
        elif m['score_dom']==m['score_ext'] :
            classement[m['equipe_dom']]['N']+=1
            classement[m['equipe_dom']]['PTS']+=2
            classement[m['equipe_ext']]['N']+=1
            classement[m['equipe_ext']]['PTS']+=2
        elif m['score_dom']<m['score_ext'] :
            classement[m['equipe_dom']]['P']+=1
            classement[m['equipe_dom']]['PTS']+=1
            classement[m['equipe_ext']]['G']+=1
            classement[m['equipe_ext']]['PTS']+=3
        if m['score_dom']==-1: # Si forfait on ne compte pas le but -1
            m['score_dom']=0
        if m['score_ext']==-1: # Si forfait on ne compte pas le but -1
            m['score_ext']=0
        classement[m['equipe_dom']]['Buts+']+=m['score_dom']
        classement[m['equipe_ext']]['Buts+']+=m['score_ext']
        classement[m['equipe_dom']]['Buts-']+=m['score_ext']
        classement[m['equipe_ext']]['Buts-']+=m['score_dom']

df = pd.DataFrame.from_dict(classement, orient='index')
df['Diff']=df['Buts+']-df['Buts-']
df.sort_values(by=['PTS','Diff'],ascending=False, inplace=True)
df['Position'] = df.reset_index().index +1
#print(df)
pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
# Saving in HTML file
html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title></head>
      <link rel="stylesheet" type="text/css" href="df_style.css"/>
      <body>
        {table}
      </body>
    </html>.
    '''
# OUTPUT AN HTML FILE
with open('Classement_actuel.html', 'w') as f:
        f.write(html_string.format(table=df.to_html(classes='mystyle',index=True,col_space=30)))

# Save classement in SQL
df.to_sql('Classement', conn, if_exists='replace', index = True)
conn.close()

print('Task completed in', time.time() - start,'seconds')
