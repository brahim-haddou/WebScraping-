from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

PATH_D = '/usr/bin/chromedriver'
driver = webdriver.Chrome(PATH_D)
data = []
for d in range(1,5):
    url = "https://www.goalzz.com/?region=-1&area=6&dd={}&mm=9&yy=2020".format(d)
    day = '{}/09/20 '.format(d)
    driver.get(url)

    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "matchesTable"))
        )
        rows = table[0].find_elements_by_tag_name("tr")
        league = ""
        match_time = ""
        equipe1 = ""
        score_equipe1 = ""
        score_equipe2 = ""
        equipe2 = ""
        match_info = ""
        for row in rows:
            if row.get_attribute('class') == "leagueRow":
                league = row.find_elements_by_tag_name("a")[0].text.rstrip("\n")
            columns = row.find_elements_by_tag_name("td")
            if len(columns) == 6:
                if columns[0].text.rstrip("\n") != "":
                    time = day + columns[0].text.rstrip("\n")
                    match_time = datetime.strptime(time, '%d/%m/%y %H:%M')
                equipe1 = columns[1].text.rstrip("\n")
                if len(columns[2].text.split(":")) == 2:
                    if columns[2].text.split(":")[0].strip() != "--":
                        score_equipe1 = int(columns[2].text.split(":")[0].strip())
                        score_equipe2 = int(columns[2].text.split(":")[1].strip())
                equipe2 = columns[3].text.rstrip("\n")
                match_info = columns[4].text.rstrip("\n")

                
                data.append([league, match_time, equipe1, score_equipe1, score_equipe2, equipe2, match_info])
    finally:
        driver.quit()


with open("data.csv", 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for i in data:
        wr.writerow(i)