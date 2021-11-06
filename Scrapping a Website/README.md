In this file we will be scrapping the website: www.xcom-shop.ru
The script of will scrap the website and find all the data about GPUs

The output of the data will be stored as a 'csv' file named output

the data collected for a single GPU is: 

store_name, gpu_model, gpu_name, fetch_ts, gpu_price, in_stock, url


# Running the script:

To run the script `python.py`, we first need to install all the requirements from `requirements.txt` using the command:

```
pip install -r server/requirements.txt
```

Then we can run script using the command:
```
python3 main.py
```

If everything run correctly you will recive an output message:
```
Job done successfully!
```

Which mean that website has been scrapped successfully, and all the data has been stored in `output.txt`

