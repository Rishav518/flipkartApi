import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/flipkart', methods=['GET'])
def scrape_flipkart():
    url = 'https://www.flipkart.com/acer-aspire-7-amd-ryzen-5-hexa-core-5500u-16-gb-512-gb-ssd-windows-11-home-4-graphics-nvidia-geforce-gtx-1650-a715-42g-gaming-laptop/p/itm56ce3828a6acc?pid=COMGCRQZQDZRA53F&lid=LSTCOMGCRQZQDZRA53FEWMIOC&marketplace=FLIPKART&fm=neo%2Fmerchandising&iid=M_c8c39d58-f7ef-4639-9291-1d8839709c82_3_H200ONZH34GS_MC.COMGCRQZQDZRA53F&ppt=pp&ppn=pp&ssid=ulz662e9c00000001707909762713&otracker=clp_pmu_v2_Acer%2BGaming%2BLaptops_2_3.productCard.PMU_V2_Acer%2BAspire%2B7%2BAMD%2BRyzen%2B5%2BHexa%2BCore%2B5500U%2B-%2B%252816%2BGB%252F512%2BGB%2BSSD%252FWindows%2B11%2BHome%252F4%2BGB%2BGraphics%252FNVIDIA%2BGeForce%2BGTX%2B1650%2529%2BA715-42G%2BGaming%2BLaptop_gaming-laptops-store_COMGCRQZQDZRA53F_neo%2Fmerchandising_1&otracker1=clp_pmu_v2_PINNED_neo%2Fmerchandising_Acer%2BGaming%2BLaptops_LIST_productCard_cc_2_NA_view-all&cid=COMGCRQZQDZRA53F'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        product_name = soup.select_one(".VU-ZEz").get_text().strip()
    except AttributeError:
        product_name = "Name not found on the page."

    try:
        price_element = soup.find('div', class_='Nx9bqj CxhGGd')
        product_current_price = price_element.get_text().strip()
    except AttributeError:
        product_current_price = "Price not found on the page."

    try:
        product_real_price = soup.find('div', class_='yRaY8j A6+E6v').get_text().strip()
    except AttributeError:
        product_real_price = "Real price not found on the page."

    try:
        product_rating = soup.find('div', class_='XQDdHH').get_text().strip()
    except AttributeError:
        product_rating = "Rating not found on the page."

    try:
        product_savings_percentage = soup.find('div', class_='UkUFwK WW8yVX').find('span').get_text().strip()
    except AttributeError:
        product_savings_percentage = "Savings percentage not found on the page."

    try:
        product_image_url = soup.find('img', class_='DByuf4 IZexXJ jLEJ7H')['src']
    except (AttributeError, KeyError):
        product_image_url = "Image source not found on the page."

    table_rows = soup.select("tr.WJdYP6.row")
    table_data = {}
    for row in table_rows:
        th = row.find("td", class_="+fFi1w col col-3-12")
        td = row.find("td", class_="Izz52n col col-9-12")
        if th and td:
            key = th.get_text().strip()
            value = td.get_text().strip()
            table_data[key] = value

    data = {
        'name': product_name,
        'image_url': product_image_url,
        'current_price': product_current_price,
        'real_price': product_real_price,
        'rating': product_rating,
        'savings_percentage': product_savings_percentage,
        'table_data': table_data
    }

    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))