In this file we will be scrapping the two websites: www.regard.ru & www.onlinetrade.ru

The script of will scrap the websites using rotating IPs by Tor

the scraping will run simultaneously to find all the data about GPUs

The output of the data will be stored as a 'csv' file named `output`

the data collected for a single GPU is:

`store_name, gpu_model, gpu_name, fetch_ts, gpu_price, in_stock, url`

# Setting up the project :

First get the directory were the main file is:
```
cd scrapping_part3/scrapping_part3/spiders
```
Then we install all the needed libraries:
```
pip install -r requirements.txt
```

# Configuring Tor

To access Tor you need to generate your uniq password, and save it
```
tor --hash-password PASSWORDHERE
```
Next, copy the generated hash and add the below lines to the end of `/etc/tor/torrc` (replace GENERATEDHASH with the hash generated):
```
ControlPort 9051
HashedControlPassword GENERATEDHASH
```

To authentic your tor requests, add the original password you used to generate the hash in 'password.txt'

# Configuring Privoxy
With your favorite editor, add the below lines at the end of `/etc/privoxy/config`
```
forward-socks5t / 127.0.0.1:9050 .
# Optional
keep-alive-timeout 600
default-server-timeout 600
socket-timeout 600
```
Now that everything is configured, all you have to do is start the services by running:
```
sudo service privoxy start
sudo service tor start
```
# Running the crawler:
To run the crawler `GPU_data_collector`, we first need to install all the requirements from `requirements.txt` using the command:

Then we can run script using the command:
```
scrapy crawl GPU_data_collector -o output.csv -t csv
```

After that all the data will be stored in `output.txt`

