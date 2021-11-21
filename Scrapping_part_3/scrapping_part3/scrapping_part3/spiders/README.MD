In this file we will be scrapping the two websites: www.regard.ru & www.onlinetrade.ru 

The script of will scrap the websites using rotating IPs by Tor

the scraping will run simultaneously to find all the data about GPUs

The output of the data will be stored as a 'csv' file named `output`

the data collected for a single GPU is: 

store_name, gpu_model, gpu_name, fetch_ts, gpu_price, in_stock, url

# The structure of the scrapping process:

first we have a list of local docker container, which form a swarm for us to use.
each one has it's own local IP. So in order to mask our IP, for each request
we will connect to the docker server. Then it will generate a Tor IP which we
will use to make the requests


# Setting up the Docker Swarm:
First we install all the needed libraries:
```
pip install -r requirements.txt
```
To initialize the docker swarm we run the command:
```
docker swarm init
```

You need to give your app a name. Here, it is set to webscrapping:

```
docker stack deploy -c docker-compose.yml webscrapping
```

To check that our containers are alive we can try this command:
```
container ls -q
```
# Running the crawler:

To run the crawler `GPU_data_collector`, we first need to install all the requirements from `requirements.txt` using the command:

Then we can run script using the command:
```
scrapy crawl GPU_data_collector -o output.csv -t csv
```

After that all the data will be stored in `output.txt`

