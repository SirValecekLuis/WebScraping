import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()

proxies = {"69.241.4.70": "80"}


def find_cheating_players():
    url_main_page = "https://lsgamerz.gameme.com/cstrike3"
    html_main_page_text = requests.get(url_main_page, proxies, verify=False).text
    soup_main_page = BeautifulSoup(html_main_page_text, "lxml")

    table_with_players = soup_main_page.find("table", class_="player_livestats")

    table_with_players_find_ct = table_with_players.find_all("tr", class_="team_a_fc")
    table_with_players_find_t = table_with_players.find_all("tr", class_="team_b_fc")
    table_with_players_find_spec = table_with_players.find_all("tr", class_="conn_players")

    player_urls_ct = []
    player_urls_t = []
    player_urls_spec = []

    for player_ct in table_with_players_find_ct:
        list_ct = str(player_ct).split()
        player_ct_url = list_ct[5].replace('href="', "")
        player_ct_url = player_ct_url.replace('"><img', "")
        player_urls_ct.append(player_ct_url)

    for player_t in table_with_players_find_t:
        list_t = str(player_t).split()
        player_t_url = list_t[5].replace('href="', "")
        player_t_url = player_t_url.replace('"><img', "")
        player_urls_t.append(player_t_url)

    for player_spec in table_with_players_find_spec:
        list_spec = str(player_spec).split()
        player_spec_url = list_spec[5].replace('href="', "")
        player_spec_url = player_spec_url.replace('"><img', "")
        player_urls_spec.append(player_spec_url)

    player_urls_list = player_urls_ct + player_urls_t + player_urls_spec
    len_player_urls_list = len(player_urls_list)

    index = 0
    for i in range(len_player_urls_list):
        try:
            url_player_page = player_urls_list[index]

            html_text = requests.get(url_player_page, proxies, verify=False).text
            soup = BeautifulSoup(html_text, "lxml")
            player = soup.find("table", class_="spacer_b")

            player_ID_find = player.find_all("tr", class_="t_fc")
            player_ID = player_ID_find[2].text

            player_name = player_ID_find[0].text

            cont_right = soup.find("div", class_="cont_right")

            player_HS_rat_find = cont_right.find_all("tr", class_="t_sc")
            player_HS_rat_find = player_HS_rat_find[2]
            player_HS_rat = str(player_HS_rat_find).split()
            player_HS_rat = player_HS_rat[6]
            player_HS_rat = player_HS_rat.replace("%", "")

            player_KD_find = cont_right.find_all("tr", class_="t_fc")
            player_KD = str(player_KD_find[2]).split()
            player_KD = player_KD[6]

            player_acc = str(player_KD_find[6]).split()
            player_acc = player_acc[6]

            try:
                player_hits_find = soup.find_all("div", class_="cont_right")
                player_hits_find = player_hits_find[4].find_all("td", class_="t_sc")

                player_hits_first = str(player_hits_find[0].text).replace(",", "")
                player_hits_second = str(player_hits_find[2].text).replace(",", "")
                player_hits_third = str(player_hits_find[4].text).replace(",", "")

                player_middle_rates_find = soup.find_all("div", class_="cont_right")
                player_middle_rates_find = player_middle_rates_find[4].find_all("td", class_="t_sc")

                player_middle_rates_first = player_middle_rates_find[1].text
                player_middle_rates_second = player_middle_rates_find[3].text
                player_middle_rates_third = player_middle_rates_find[5].text

            except:
                player_hits_first = None
                player_hits_second = None
                player_hits_third = None

                player_middle_rates_first = None
                player_middle_rates_second = None
                player_middle_rates_third = None

            may_be_cheating = False
            high_HS = False
            high_KD = False
            text_error = None
            text_error_show = None
            try:
                if int(player_hits_first) > 40:
                    if float(player_middle_rates_first) > 50:
                        may_be_cheating = True

                if int(player_hits_second) > 40:
                    if float(player_middle_rates_second) > 50:
                        may_be_cheating = True

                if int(player_hits_third) > 40:
                    if float(player_middle_rates_third) > 50:
                        may_be_cheating = True

            except TypeError:
                text_error_show = True
                cannot_be_loaded = f"I'm sorry, but I can't load player's number of shoots and middle % ratio."
                text_error = (
                    f"{player_name}, {player_ID}\n"
                    f"Total HS ratio: {player_HS_rat}%, KD: {player_KD}, Accuracy: {player_acc}\n"
                    f"{cannot_be_loaded}\n")

            if float(player_KD) > 4.2:
                high_KD = True

            if float(player_HS_rat) > 52:
                high_HS = True

            text = (
                f"{player_name}, {player_ID}\n"
                f"Total HS ratio: {player_HS_rat}%, KD: {player_KD}, Accuracy: {player_acc}\n"
                f"Number of shoots: {player_hits_first}, mid %: {player_middle_rates_first}\n"
                f"Number of shoots: {player_hits_second}, mid %: {player_middle_rates_second}\n"
                f"Number of shoots: {player_hits_third}, mid %: {player_middle_rates_third}\n"
            )

            printed = False
            if may_be_cheating:
                print(text)
                printed = True

            if high_HS or high_KD:
                if printed:
                    pass
                elif text_error_show:
                    print(text_error)
                else:
                    print(text)
        except:
            pass
        index += 1


if __name__ == "__main__":
    while True:
        find_cheating_players()
        time_wait = 600
        print(f"Waiting {time_wait / 60} mins. ")
        time.sleep(time_wait)

