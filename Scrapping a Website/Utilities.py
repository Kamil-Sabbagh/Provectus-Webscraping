from bs4 import BeautifulSoup
import time
import requests
import csv

#The data for out header for the HTML pages
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}


def find_the_number_of_pages(site):
    #We will will make a get request to the HTML of the page so we can scrap the data from it
    try:
        response = requests.get(site, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()
    soup = BeautifulSoup(response.text, "html.parser")

    #After we have the HTML file we will see how many pages from the website we need to scrap
    pages = soup.find('div', class_="navigation block-universal clear gray")
    return str(pages).count('list_page') + 1

def find_all_the_products(site):
    #We will read the page to by doing a GET request for the specified page
    try:
        response = requests.get(site, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()
    soup = BeautifulSoup(response.text, "html.parser")

    # now we find all the products using the tag 'div' and class 'wrap catalog_item'
    products = soup.find_all('div', class_="wrap catalog_item")
    return products

def get_all_data_of_product(product):
    # We can find the name of the product in tag 'div' class 'name'
    string = product.find('div', class_="name").text
    pro_name = string[:string.find(('(')) - 1]

    # We can find the price of product in tag 'div' class 'price'
    pro_price = product.find('div', class_="price").find('div', class_="new").text.replace(' ', '')[:-4]

    # We can find if the product is available in tag 'div' class 'buy'
    in_stock = str(product.find('div', class_="buy"))
    available = in_stock[in_stock.find('value="') + 7]

    # We also need to save the time we did scrapping
    ft = time.time()

    # We can find the URL of the product in tag 'div' class 'name'
    pro_url = product.find('div', class_="name")
    links_with_text = []
    for a in pro_url.find_all('a', href=True):
        if a.text:
            links_with_text.append(a['href'])
    url = "https://www.xcom-shop.ru/" + links_with_text[0]


    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()

    pro_type = ''
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        infos = soup.find_all('li', class_='product-block-description__item')
        for info in infos:
            temp = info.find('div', class_='product-block-description__first-elem').text.strip()
            if temp == 'Тип' :
                pro_type = info.find('div', class_='product-block-description__second-elem').text
                break

    except IndexError:
        pro_type = None



    return pro_type, pro_name, ft, available, pro_price, url


def store_data(  shop_name, pro_type, pro_name, ft, available, pro_price, url):
    #We will create a dictionary to reutrn
    data = {'store_name': [], 'gpu_model': [], 'gpu_name': [], 'fetch_ts': [], 'gpu_price': [], 'in_stock': [], 'url': []}

    #and store all the data inside it
    data['store_name'].append(shop_name)
    data['gpu_model'].append(pro_type)
    data['gpu_name'].append(pro_name)
    data['fetch_ts'].append(ft)
    if available:
        data['in_stock'].append(True)
    else:
        data['in_stock'].append(False)
    data['gpu_price'].append(pro_price)
    data['url'].append(url)

    return data

def save_in_csv(data, output):
    #we open the csv file
    with open(output, 'w', newline='') as csvfile:
        #in the first line we write the header values which are the same as the keys in our dictionary
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        writer.writeheader()
        #then we save each row by itself
        for value in range(len(data['store_name'])):
            row = {'store_name': [], 'gpu_model': [], 'gpu_name': [], 'fetch_ts': [], 'gpu_price': [], 'in_stock': [],
                   'url': []}
            for key in data.keys():
                row[key] = data[key][value]
            writer.writerow(row)
