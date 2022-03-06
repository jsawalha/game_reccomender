import requests
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.dekudeals.com/items/"
COOKIES = {'rack.session': 'BAh7DUkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU2OWJkMzAzMTAyZDc0MzRlNzQ4ODQ5MWY4YTI5Y2VkNDNmZmEzNzEzNGU0OGM1MzIzN2I4OGNmZGIzYjg4NDE4BjsARkkiCWNzcmYGOwBGSSIxc00xRU5MYk9xd3lEdzBsbkRWVmJ5cHR5Wlc3ZW93d2wxdnZQQkhnbStaMD0GOwBGSSILc291cmNlBjsARiIcaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9JIgxsYW5kaW5nBjsARkkiMi9pdGVtcy90aGUtbGVnZW5kLW9mLXplbGRhLWJyZWF0aC1vZi10aGUtd2lsZAY7AFRJIgxjb3VudHJ5BjsARkkiB2NhBjsAVEkiDl9fRkxBU0hfXwY7AEZ7AEkiFXBsYXRmb3JtX2ZpbHRlcnMGOwBGewk6C3N3aXRjaDoIYWxsOghwczU7CToIcHM0Owk6DXhib3hfb25lOwlJIg1zcGVjaWFscwY7AEZbAA%3D%3D--1ef930704d63dc368631d2dd6e10afc15bf70b8b'}


#This is scraping all the data from each page, for each game, and saving it in a csv file
def scrape_details(URL, COOKIES):
    key_check = ['Released', 'Genre', 'Number of players', 'Developer', 
             'Publisher', 'Download size', 'Metacritic', 'How Long To Beat', 
             'ESRB Rating', 'Play modes', 'Languages', 'Description']

    game_details = {}


    req = requests.get(URL, cookies=COOKIES)

    if req.status_code != 200:
        return None
    
    soup = BeautifulSoup(req.content, "html.parser")

    #Get title
    game_details["title"] = soup.find('span', class_ = "display-5").get_text()

    # Get all variables in the side bar on the left of the page
    det_scrape = soup.find_all('li', class_ = 'list-group-item')

    for det in det_scrape:
        det = det.get_text()
        if ':' in det:
            game_details[det.split(':')[0]] = det.split(':', 1)[1][1:]
        else:
            continue

    #Get description
    try:
        des_scrape = soup.find('div', class_ = 'description').get_text().replace('\n', '')
    except:
        des_scrape = 'NaN'

    game_details['Description'] = des_scrape

    for keys in key_check:
        if keys in game_details.keys():
            pass
        else:
            game_details[keys] = 'NaN'
    
    return game_details



# Main function
if __name__ == "__main__":
    URL = "https://www.dekudeals.com/items/"
    COOKIES = {'rack.session': 'BAh7DUkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU2OWJkMzAzMTAyZDc0MzRlNzQ4ODQ5MWY4YTI5Y2VkNDNmZmEzNzEzNGU0OGM1MzIzN2I4OGNmZGIzYjg4NDE4BjsARkkiCWNzcmYGOwBGSSIxc00xRU5MYk9xd3lEdzBsbkRWVmJ5cHR5Wlc3ZW93d2wxdnZQQkhnbStaMD0GOwBGSSILc291cmNlBjsARiIcaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9JIgxsYW5kaW5nBjsARkkiMi9pdGVtcy90aGUtbGVnZW5kLW9mLXplbGRhLWJyZWF0aC1vZi10aGUtd2lsZAY7AFRJIgxjb3VudHJ5BjsARkkiB2NhBjsAVEkiDl9fRkxBU0hfXwY7AEZ7AEkiFXBsYXRmb3JtX2ZpbHRlcnMGOwBGewk6C3N3aXRjaDoIYWxsOghwczU7CToIcHM0Owk6DXhib3hfb25lOwlJIg1zcGVjaWFscwY7AEZbAA%3D%3D--1ef930704d63dc368631d2dd6e10afc15bf70b8b'}

    href_links = np.load('../game_price_scrap/href_links.npy')
    print(len(href_links))

    new_df = pd.DataFrame()
    counter = 1
    for k in href_links:
        URL_add = URL + k
        print("Now on:", k)
        new_game = scrape_details(URL_add, COOKIES)
        df_dic = pd.DataFrame([new_game])
        new_df = pd.concat([new_df, df_dic], ignore_index=True)
        counter = counter + 1
        print(f"On game number {counter} \t of {len(href_links)}")
        # print(new_df.head(5))
    print('saving.....')
    new_df.to_csv("/DATA/game_price_scrap/results_scraping.csv", index=False)
    print("finished")



