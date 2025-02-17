import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://store.steampowered.com/search/?specials=1&page="

def get_game_data(page):
   
    response = requests.get(URL + str(page))
    soup = BeautifulSoup(response.text, "html.parser")
    
    games = []
    for game in soup.select(".search_result_row"):
        name = game.select_one(".title").text
        price = game.select_one(".discount_final_price")
        price = price.text if price else "Free"
        
        discount = game.select_one(".search_discount span")
        discount = discount.text.strip("-") if discount else "0%"

        reviews = game.select_one(".search_review_summary")
        reviews = reviews["data-tooltip-html"].split("<br>")[0] if reviews else "No reviews"

        games.append([name, price, discount, reviews])
    
    return games

def save_to_excel(data):

    df = pd.DataFrame(data, columns=["Name", "Price", "Discount", "Reviews"])
    df.to_excel("steam_games.xlsx", index=False)
    print("Data saved to steam_games.xlsx!")

def main():
   
    pages = int(input("How many pages to scrape? "))
    all_games = [game for page in range(1, pages + 1) for game in get_game_data(page)]
    
    if all_games:
        save_to_excel(all_games)
    else:
     	 print("No data found!")

if __name__ == "__main__":
    main()
