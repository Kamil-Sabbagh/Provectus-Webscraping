import Utilities



#we define the url of the website we want to scrape
main_url = "https://www.xcom-shop.ru/catalog/kompyuternye_komplektyyuschie/videokarty/"
shop_name = 'xcom-shop'


print(f"You are scraping the website {main_url} to find data about GPUs, Your data will be stored in output.csv")

#we get the number of pages using the utility function find_the_number_of_pages
number_of_pages = Utilities.find_the_number_of_pages(main_url)

#here we create the dictionary that will contain our data
data = {'store_name': [], 'gpu_model': [], 'gpu_name': [], 'fetch_ts': [], 'gpu_price': [], 'in_stock': [], 'url': []}

#For each page on the website that has GPUs we will scrap it one by one
for page in range(1 , number_of_pages+1) :

    #we edit the URL for each page
    url = f"https://www.xcom-shop.ru/catalog/kompyuternye_komplektyyuschie/videokarty/?list_page={page}"

    #We get the list of products using the utility function find_all_products
    List_of_products = Utilities.find_all_the_products(url)

    #then for each product we have to scrap all the needed data
    for product in List_of_products:

        '''
         We will use the type given to do a simple filtering for the GPUs.
         Since the website may contain other products on these pages such as cables, batteries, and so on, we need to filter only the GPUs
         So here we do the filtering, if the product type in not a Video Card we discard the item
        '''
        pro_type = product.find('div', class_="type").text
        if pro_type != "Видеокарта PCI-E":
            continue

        #we get all the data of the product using the utility function get_all_data_of_product
        pro_type, pro_name, ft, available, pro_price, url = Utilities.get_all_data_of_product(product)

        #and we store the data
        product_data = Utilities.store_data(shop_name, pro_type, pro_name, ft, available, pro_price, url)
        for label in product_data :
            data[label].append(product_data[label][0])


#print(data)


output = 'output.csv'
Utilities.save_in_csv(data , output)

print("Job done successfully!")



