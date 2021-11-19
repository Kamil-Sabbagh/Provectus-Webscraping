In this file we will be scrapping the two websites: www.regard.ru & www.onlinetrade.ru 


The script of will scrap the websites simultaneously and find all the data about GPUs

The output of the data will be stored as a 'csv' file named `output`

the data collected for a single GPU is: 

store_name, gpu_model, gpu_name, fetch_ts, gpu_price, in_stock, url


# Running the crawler:


To run the crawler `GPU_data_collector`, we first need to install all the requirements from `requirements.txt` using the command:

```
pip install -r requirements.txt
```

Then we can run script using the command:
```
scrapy crawl GPU_data_collector -o output.csv -t csv
```

After that all the data will be stored in `output.txt`

