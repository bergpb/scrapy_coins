import os
import re
import pymongo
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

from dotenv import load_dotenv
load_dotenv()

client = pymongo.MongoClient(os.getenv('MONGO_CON'))

db = client.ravena
collection = db.coins

i = 0
data = []
ripple = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=brl"
litecoin = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=brl"
ethereum = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=brl"

# from mercadocotacao
mercado = "https://mercadocotacao.com"
content = requests.get(mercado).content
soup = BeautifulSoup(content.decode("utf-8"), "html.parser")
coins = soup.find("div", class_="home_conv_carrocel")
images = [
            "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/dolar.svg",
            "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/dolar.svg",
            "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/dolar.svg",
            "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/euro.svg",
            "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/bitcoin.svg",
            "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/libra.svg",
            "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/peso.svg",
        ]
for data_coins in coins.find_all("div", class_="home_conv_carrocel_item"):
    name = data_coins.find("a")["title"].split(" Hoje")[0]
    value = data_coins.find("span").text
    date = dt.now()
    data.append({
                 "name": name,
                 "image": images[i],
                 "value": re.search("\d+[,.]\d+[,]?\d+", value)[0],
		         "date": dt.now()
                })
    i += 1

# from api
rip = requests.get(ripple).json()['ripple']['brl']
lit = requests.get(litecoin).json()['litecoin']['brl']
eth = requests.get(ethereum).json()['ethereum']['brl']

coins_value = [rip, lit, eth]
coins_name = ['Ripple', 'Litecoin', 'Ethereum']
coins_images = [
    "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/ripple.svg",
    "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/litecoin.svg",
    "https://financeone-statics.sfo2.cdn.digitaloceanspaces.com/img/moedas/ethereum.svg",
]
for i in range(len(coins_name)):
    data.append({
                 "name": coins_name[i],
                 "image": coins_images[i],
                 "value": coins_value[i],
		         "date": dt.now()
                })


# usd = "https://apilayer.net/api/live?access_key=cb8a60847541bdb828ff4274697cdc36&currencies=BRL&source=USD"
# eur = "https://apilayer.net/api/live?access_key=cb8a60847541bdb828ff4274697cdc36&currencies=BRL&source=EUR"
# gbp = "https://apilayer.net/api/live?access_key=cb8a60847541bdb828ff4274697cdc36&currencies=BRL&source=GBP"
# ars = "https://apilayer.net/api/live?access_key=cb8a60847541bdb828ff4274697cdc36&currencies=BRL&source=ARS"
# btc = "https://apilayer.net/api/live?access_key=cb8a60847541bdb828ff4274697cdc36&currencies=BRL&source=BTC"


# finance = "https://financeone.com.br/moedas/cotacoes-do-real-e-outras-moedas"
# content = requests.get(finance).content
# soup = BeautifulSoup(content.decode("utf-8"), "html.parser")
# coins = soup.find("div", class_="stocks lessContent")
# for data_coins in coins.find_all("div"):
#     image = data_coins.find("img")["src"]
#     name = data_coins.find("b").text
#     print(data_coins)
#     value = re.search("\d+[,.]\d+[,]?\d+", data_coins.text)[0]
#     data.append({
#                  "image": image,
#                  "name": name,
#                  "value": value,
# 		         "date": dt.now()
#                 })

new_entries = collection.insert_many(data)
print('---------------------------------------------------')
print('Coins saved at: {}'.format(dt.now().strftime("%d/%m/%Y - %H:%M:%S")))
print('Multiple posts: {}'.format(new_entries.inserted_ids))
print('---------------------------------------------------')

