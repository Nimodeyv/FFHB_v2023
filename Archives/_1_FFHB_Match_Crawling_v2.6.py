from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
import time
import re
import csv
import sqlite3
import glob, os
#
start = time.time() # To measure time

#URL=input('Coller le lien URL de la poule à analyser:')

# Liste de tous les matchs extraits
lst= glob.glob(".\FDM\*.pdf")
print("Nombre de matchs analysés: ",len(lst))
lst = [l.replace('FDM\\',"").replace('.sqlite','.pdf') for l in lst]

# install chrome web driver https://sites.google.com/a/chromium.org/chromedriver/downloads
PATH = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Pointing to the targeted poule
driver.get("https://www.ffhandball.fr/fr/competition/20405#poule-109164")
time.sleep(1)

# Close the window that is opening when opening from chrome machine
Path = '//*[@id="didomi-notice-agree-button"]'
driver.find_element(By.XPATH, Path).click()
time.sleep(1)

# Sélectionne le championnat et la journée
content = driver.find_element_by_class_name('l-page-content')
content.click()
time.sleep(2)
counter = 0
TXT= list()
ans=input('Entre la premiere journée (incluse) à scraper (par defaut 1):')
if ans=="": j0=1
else: j0=int(ans)
ans=input('Entre la derniere journée (incluse) à scraper (par défaut 22):')
if ans=="": j1=22
else: j1=int(ans)

dir=os.path.abspath('.\FDM')

for j in range(j0-1,j1):
    try:
        XPATH = "//*[@class='s-fixtures-calendar-day ' and text()="+str(j+1)+"]"
        journee = driver.find_element_by_xpath(XPATH)
        journee.click()
        time.sleep(2)
    except:
        XPATH = "//*[@class='s-fixtures-calendar-day s-fixtures-calendar-day--current-date' and text()="+str(j+1)+"]"
        journee = driver.find_element_by_xpath(XPATH)
        journee.click()
        time.sleep(2)
    # Affiche le titre et le contenu texte de la page
    text = driver.page_source
    text2=text.split('<div class="s-fixtures-table-row">')
    #
    if counter == 0 :
        print(driver.title)
        Ligue = re.findall('<div class="m-standings__title">(.+?)</div>',text) # Ligue
        print(Ligue[0])
        Poule = re.findall('<span class="js-dropdown__current b-dropdown-custom__button">(.+?)</span>',text) # Poule
        print(Poule[0])
    Periode = re.findall('<div class="s-fixtures-table__title">(.+?)</div>',text) # Date période des journées
    print(Periode)
    #
    for l in text2[1:]:
            m = dict()
            Date = re.findall('<p class="s-fixtures-table-cell-row__date">(.+?)</p>',l) # Date journée
            Match = re.findall('<p class="s-fixtures-table-cell-row__name">(.+?)</p>',l) # Match
            Score = list()
            for i in re.findall('<p class="s-fixtures-table-cell-row__result(.+?)</p>',l):
                Score.append(re.findall('>(.+)',i))
            Infos = re.findall('<p class="s-fixtures-table-cell-list__item">(.+?)</p>',l) # Match
            FDM = re.findall('<a href="(.+?)" class="s-fixtures-table-cell-button" target="_blank">FDM</a>',l) # Lien fichier feuille de match
            title = str(j+1)+"_"+Match[0].replace('/','&')+"-"+Match[1].replace('/','&')+".pdf"
            print(Date, Match,Infos)
            print(FDM,title)
            if (FDM != []) & (title not in lst):
                path = os.path.join(dir,title)
                urlretrieve(FDM[0],path)
                # Enregistre le match sous pdf
            m['Periode']=Periode[0]
            m['Journee']=j+1
            m['Date']=Date[0]
            m['fichier']=title
            m['equipe_dom']=Match[0].replace('/','&')
            m['equipe_ext']=Match[1].replace('/','&')
            m['lieu']=Infos[0]+" "+Infos[1]+" "+Infos[2]
            m['arbitres']=Infos[4]+" "+Infos[5]
            if Score[0][0]=='FO':
                m['score_dom']=-1 # On met un score de -1 si forfait
                m['score_ext']=int(Score[1][0])
                m['diff_buts']=0-int(Score[1][0])
            elif Score[1][0]=='FO':
                m['score_dom']=int(Score[0][0])
                m['score_ext']=-1
                m['diff_buts']=int(Score[0][0])-0
            elif Score[0][0]!='--' and Score[1][0]!='--':
                m['score_dom']=int(Score[0][0])
                m['score_ext']=int(Score[1][0])
                m['diff_buts']=int(Score[0][0])-int(Score[1][0])
            else:
                m['score_dom']=""
                m['score_ext']=""
                m['diff_buts']=""
            TXT.append(m)
    counter = 1
driver.close()
# SAVE in SQLITE Files
conn = sqlite3.connect('Championnat_U18_GrandEst.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Matchs  (
    fichier TEXT NOT NULL PRIMARY KEY UNIQUE,
    Journee INTEGER,
    Periode TEXT,
    Date TEXT,
    equipe_dom TEXT,
    equipe_ext TEXT,
    score_dom INTEGER,
    score_ext INTEGER,
    diff_buts INTEGER,
    lieu TEXT,
    arbitres TEXT
    )''')
for m in TXT:
    cur.execute('''INSERT OR REPLACE INTO Matchs (fichier,Journee, Periode, Date, equipe_dom, equipe_ext,score_dom,score_ext,diff_buts,lieu,arbitres)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (m['fichier'],m['Journee'],m['Periode'],m['Date'],m['equipe_dom'],m['equipe_ext'],m['score_dom'],m['score_ext'],m['diff_buts'],m['lieu'],m['arbitres']))
#
conn.commit()
conn.close()
# SAVE IN CSV FILE
#file = "Matchs_"+Ligue[0]+".csv"
#keys = TXT[0].keys()
#a_file = open(file, "w")
##dict_writer = csv.DictWriter(a_file, keys)
#dict_writer.writeheader()
#dict_writer.writerows(TXT)
#a_file.close()
#
print('Task completed in', time.time() - start,'seconds')
