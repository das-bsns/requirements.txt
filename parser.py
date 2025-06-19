import requests
from bs4 import BeautifulSoup

def parse_ned_kg():
    url = "https://ned.kg/admin?property_action_category_id=120&rooms[]=2&property_area[]=31&price_low=94000&price_max=100000&property_condition[]=292"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = []

    cards = soup.select(".property")
    for card in cards:
        try:
            title = card.select_one(".property-title a").text.strip()
            link = "https://ned.kg" + card.select_one(".property-title a")["href"]
            image = card.select_one("img")["src"]
            price = card.select_one(".property-price").text.strip()
            desc = card.select_one(".property-location").text.strip()
        except Exception:
            continue

        listings.append({
            "title": title,
            "link": link,
            "image": image,
            "price": price,
            "desc": desc
        })

    return listings
