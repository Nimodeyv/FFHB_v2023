# FFHB_2023
French Handball Championship Analysis
#
These Jupyter notebooks are scrapping informations and making analysis of one French division of Handball.
It is an investigation and demo of various Python libraries capabilities. In every notebook I will mention which new library capability is used.
#
#
_10_FFHB_Match_Crawling.ipynb
This notebook is scrapping data from the internet website and uses sqlite3, selenium and ipywidgets libraries.
It scrapp informations on matchs (ie. dates, teams, location, referee and score if matchs already took place ). All informations are stored in a SQL file 'Championnat_U18_GrandEst.sqlite'
#
![10](https://github.com/Nimodeyv/FFHB_v2023/tree/master/ANALYSE/10.jpg)
#
_20_FFHB_Calcul_Classement.ipynb
#
This notebook is analysing the different matchs from the sql db and making ranking of the championship. It uses pandas library.
It stores the ranking in a HTML table file under the path './ANALYSE/Classement_actuel.html'
#
_30_Planning_Match_U18.ipynb
This notebook is building from the selected team a planning the different matchs done and those which are coming. It uses icalendar library.
It stores output in 3 different files:
    './PLANNING/Planning_des_Matchs.html' is the overall full championship planning
    './PLANNING/EPINAL U18M_Planning_des_Matchs.html' every team selected will have its own planning file in HTML format (here team of EPINAL)
    './PLANNING/EPINAL U18M_Planning_des_Matchs.ics' every team selected will have its own planning file in HTML ics ie. univeral calendar fromat, to be used in outlook or other
#
_31_Plotting_address_on_maps_v1.ipynb
This notebook is plotting on maps the different match address and informations. It uses geopandas and folium.
Output are 2 maps in HTML format:
    './ANALYSE/Gymnases.html' is plotting on a map all the different locations of matchs
    './ANALAYSE/Championnat_U18.html' is plotting on a map all the different location and match information of the championship for the team of EPINAL
#
_40_Extract_Save_Match_in_SQL.ipynb
This notebok is extracting from every Match report (in format of pdf) the list of actions per team and per player. It is storing all these actions into the same sql file 'Championnat_U18_GrandEst.sqlite' but in a different table. It uses pdfplumber library.
#
_50_Analyse_Championnat.ipynb
This notebook is making a more analysis of the matchs and plot a summary plot show all the match, ranking and evolution of each match along the time.
It uses Matplotlib library.
Output is an image plot:
    './ANALYSE/Analyse_Equipes_U18.png'
#
_60_Analyse_joueurs.ipynb
This notebook is making an analysis of the different players from this division.
#
_70_Analyse_equipes.ipynb
This notebook is making some more detailed analysis per team.
Output file is :
    './ANALYSE/{name_of_team}.jpg'
#
_80_Plot_Match.ipynb
This notebook is plotting for each selected match a graph showing each action. When video of the match was recorded, it is also merging the different video to produce one video per half-time
It is using moviepy and cv2 library
Output are:
    '{match].html' which is the plot of the match
    '{match}.mp4' which are 2 video, one for each half time.
    
    
  
