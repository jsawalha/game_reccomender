import requests
import numpy as np
from bs4 import BeautifulSoup

#this is the url + extention we want to scrape
URL = "https://www.dekudeals.com/items?filter[type]=game"
#We want to set cookies to include PS4, PS5, XBOX and Nintendo games
COOKIES = {'rack.session': 'BAh7DUkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb246OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkU2OWJkMzAzMTAyZDc0MzRlNzQ4ODQ5MWY4YTI5Y2VkNDNmZmEzNzEzNGU0OGM1MzIzN2I4OGNmZGIzYjg4NDE4BjsARkkiCWNzcmYGOwBGSSIxc00xRU5MYk9xd3lEdzBsbkRWVmJ5cHR5Wlc3ZW93d2wxdnZQQkhnbStaMD0GOwBGSSILc291cmNlBjsARiIcaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS9JIgxsYW5kaW5nBjsARkkiMi9pdGVtcy90aGUtbGVnZW5kLW9mLXplbGRhLWJyZWF0aC1vZi10aGUtd2lsZAY7AFRJIgxjb3VudHJ5BjsARkkiB2NhBjsAVEkiDl9fRkxBU0hfXwY7AEZ7AEkiFXBsYXRmb3JtX2ZpbHRlcnMGOwBGewk6C3N3aXRjaDoIYWxsOghwczU7CToIcHM0Owk6DXhib3hfb25lOwlJIg1zcGVjaWFscwY7AEZbAA%3D%3D--1ef930704d63dc368631d2dd6e10afc15bf70b8b'}


def get_pg_num(URL, COOKIES):
    
    req = requests.get(URL, cookies=COOKIES)
    if req.status_code != 200:
        return None
    
    soup = BeautifulSoup(req.content, "html.parser")

    pg_num = -1
    for page_list in soup.find_all("ul", class_="pagination"):
        for link in page_list.find_all("a", class_="page-link"):
            try:
                if "page=" in link["href"]:
                    pageNum = -1
                    try:
                        pageNum = int(str(link["href"]).replace("?filter[type]=game&page=",""))
                        pg_num = np.max((pg_num, pageNum))
                    except:
                        pageNum = -1
            except:
                pass

    ItemNumber = -1
    item_info = soup.find_all("div", class_='pagination_controls')[0].get_text()
    try:
        ItemNumber = int(str(item_info).replace("\n", "").split("\uf05312")[0].split("of")[1].strip())
    except:
        ItemNumber = -1

    return pg_num, ItemNumber

def game_link_parser(pg_num = -1):

    game_links = []

    full_url = URL + '&page=' + str(pg_num)
    req = requests.get(full_url, cookies=COOKIES)
    if req.status_code == 200:
            soup = BeautifulSoup(req.content, "html.parser")
    
    for link in soup.find_all('a', class_ = 'main-link'):
        try:
            game_links.append(link['href'].split('/items/')[1])
        except:
            pass
    
    return game_links

#Main function
if __name__ == "__main__":
    pg_num, item_num = get_pg_num(URL, COOKIES)
    print(item_num)
    game_links_final = []
    for k in range(1, pg_num):
        item_list = game_link_parser(k)
        for item in item_list:
            print(item)
            game_links_final.append(item)
        print(f"Page: {k} \t of {pg_num}")

    
    print("Saving files to numpy...")
    np.save("../game_price_scrap/href_links.npy", game_links_final)



