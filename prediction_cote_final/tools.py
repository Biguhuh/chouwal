
import requests
import pandas as pd
from bs4 import BeautifulSoup


#creer une fonction pour voir a partir de quelle heure on peut avoir les cotes en ligne et au borne
def chek_cote():
    pass

    
#scrapper toute les cource du jour pour rendre un df a vec l'heure de la course et quelque info 
def scrapper_les_heures():
    
    url = 'https://www.pmu.fr/turf/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    data = []
    courses = soup.select("div[data-testid='CourseCardContainer']")

    for course in courses:
        rencontre_numero_div = course.select_one("div[data-testid='courseNumberCard'] > div:nth-child(1)")
        rencontre_numero = rencontre_numero_div.text if rencontre_numero_div is not None else None

        course_numero_div = course.select_one("div[data-testid='courseNumberCard'] > div:nth-child(2)")
        course_numero = course_numero_div.text if course_numero_div is not None else None

        heure_depart_div = course.select_one("div[class*='css-901oao r-11o462g r-vnw8o6 r-1b43r93 r-1cwl3u0']")
        heure_depart = heure_depart_div.text if heure_depart_div is not None else None
        
        type_course_div = course.select_one("div[class*='css-901oao css-bfa6kz r-1dnsj32 r-vnw8o6 r-1enofrn r-1f529hi r-kc8jnq']")
        type_course = type_course_div.text if type_course_div is not None else None

        data.append({"rencontre_numero": rencontre_numero,
                    "course_numero": course_numero,
                    "heure_depart": heure_depart,
                    "type_course": type_course})

    df = pd.DataFrame(data)
    return df


