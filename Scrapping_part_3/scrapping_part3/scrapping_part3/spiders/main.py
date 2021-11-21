import scrapy
import time
from requests import get


# Create the class for our crawler
class GpuDataScrapper (scrapy.Spider):

    # Naming the crawler
    name = "GPU_data_collector"

    # Then we define the URLs of the websites we are going to scrape
    start_urls = [
        'https://www.regard.ru/catalog/group4000/page2.htm',
        'https://www.onlinetrade.ru/catalogue/videokarty-c338/',
        ]

    # Settings for browsing
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) ' \
                 'Gecko/20100101 Firefox/47.3'

    # First function which will be invoked
    def start_requests(self):
        # We provide the urls to scrape
        urls = [
            'https://www.regard.ru/catalog/group4000/?page0.htm',
            'https://www.onlinetrade.ru/catalogue/videokarty-c338/',
        ]

        '''
        Since we are going to scrape to websites, it will prove useful to
        create Xpath selectors. We can use the same code for different
        websites, the only difference is the Xpath selector parsed.
        '''
        xpath_selectors = [
            {
                'parser': self.parse_all_pages,
                'website_url': 'https://www.regard.ru',
                'website_name': 'regard',
                'page_selector': "//div[@class='content']/"
                                 "div[@class='pagination']/a/@href",
                'item_name': "//div[@class='block']/div/div[2]/"
                             "a[@class='header']/text()",
                'item_model': "//div[@id='tabs-1']/table/tr[6]/"
                              "td[2]/text()",
                'item_price': "//div[@class='block']/div/"
                              "div[@class='aheader']/span/@data-price",
                'item_url': "//div[@class='block']/div/"
                            "div[@class='block_img']/a/@href",
                'item_stocked': "//div[@class='action_block left']/div/div"
                                "[@class='goodCard_inStock_button"
                                " inStock_available']/text()",
                'data': {
                    'store_name': '',
                    'gpu_model': '',
                    'gpu_name': '',
                    'fetch_ts': '',
                    'price': '',
                    'url': '',
                          },

            },

            {
                'parser': self.parse_by_page,
                'website_url': 'https://www.onlinetrade.ru/catalogue/'
                               'videokarty-c338/',
                'website_name': 'onlinetrade',
                'next_page_url': "//div[@class='paginator__links']/a[normaliz"
                                 "e-space(@title)='Следующие 15 товаров']"
                                 "/@href",
                'item_name': "//a[normalize-space(@class)='indexGoods__item__"
                             "name indexGoods__item__name__3lines']/text()",
                'item_model': "//div[@class='productPage__shortProperties']/ul"
                              "[@class='featureList columned']/li[@class="
                              "'featureList__item'][1]/text()",
                'item_price': "//span[normalize-space(@class)='price regular j"
                              "s__actualPrice' or contains(@class, 'price js__"
                              "actualPrice')]/text()",
                'item_url': "//a[normalize-space(@class)='indexGoods__item__na"
                            "me indexGoods__item__name__3lines']/@href",
                'item_stocked': True,
                'data': {
                    'store_name': '',
                    'gpu_model': '',
                    'gpu_name': '',
                    'fetch_ts': '',
                    'price': '',
                    'url': '',
                        }
            }


        ]

        # We create a zip between the urls and the xpaths
        # we have created for each website
        for url, xpath_selector in zip(urls, xpath_selectors):
            # and loop through them one by one
            yield scrapy.Request(url=url,
                                 callback=xpath_selector.get("parser"),
                                 meta=xpath_selector)

    # Parse by page function will allow us to scrape one page after the other,
    # for example if there is an option for a next bottom.
    def parse_by_page(self, response):

        # We get the url of the next page
        next_page = response.xpath(response.meta.get('next_page_url')).get()
        if next_page:
            url = next_page
            # If the url is not absolute url, we add the url of the GPUs page
            if response.meta.get('website_name') not in url:
                url = response.meta.get('website_url') + next_page

            # We scrape the data from the current page
            yield scrapy.Request(url=url, callback=self.parse_a_page,
                                 dont_filter=True, meta=response.meta)

            # Then we move to the next page, by calling
            # the same function and passing the url
            yield scrapy.Request(url=url, callback=self.parse_by_page,
                                 dont_filter=True, meta=response.meta)

    # This function help us to get all the links of
    # all the pages and then go by them one by one

    def parse_all_pages(self, response):

        # So we first get all the links
        pages = response.xpath(response.meta.get('page_selector')).getall()

        for page in range(1, len(pages)+1):

            # We construct the absolute url by add
            # the GPUs main page and the page number
            url = response.meta.get('website_url') + pages[page-1]
            # And then we scrape the data from the page
            yield scrapy.Request(url=url, callback=self.parse_a_page,
                                 dont_filter=True, meta=response.meta)
            break

    # We use the function to get the
    # data of a GPU from a page

    def parse_a_page(self, response):

        # We extract all the available data from the main page
        name = response.xpath(response.meta.get('item_name')).getall()
        price = response.xpath(response.meta.get('item_price')).getall()
        url = response.xpath(response.meta.get('item_url')).getall()

        # Then for each item we found we save it's data
        # so we cab yield it as a dictionary later on
        for item in range(len(name)):

            item_abs_url = response.meta.get('website_url') + url[item]
            response.meta.get('data')['store_name'] = response.meta.get('website_name')
            response.meta.get('data')['gpu_name'] = name[item]
            response.meta.get('data')['fetch_ts'] = time.time()
            response.meta.get('data')['price'] = price[item]
            response.meta.get('data')['url'] = item_abs_url

            '''
            Since not all the data are available in the main page.
            We need to access the url for the product and scrape
            the rest of the data
            '''
            yield scrapy.Request(item_abs_url,
                                 meta=response.meta,
                                 callback=self.parse_new, )

    # This function will help us collect extra data of an item
    # from the specific item page

    def parse_new(self, response):
        # So we need to know if we need to check the availability of the
        # 'in_stock' data, if it does not exist we assume it to be true
        if response.meta.get('item_stocked') is not True:
            stocked = response.xpath(response.meta.get('item_stocked')).get()
            if stocked == 'в наличии':
                response.meta.get('data')['in_stock'] = True
            else:
                response.meta.get('data')['in_stock'] = False
        else:
            response.meta.get('data')['in_stock'] = True

        # Finally we scrape the model name
        model = response.xpath(response.meta.get('item_model')).get()
        # And strip it from the '\xa0'tag the
        # might exist from the html response
        model = model.replace(u'\xa0', u' ')
        response.meta.get('data')['gpu_model'] = model
        #ip = response.meta.get("proxy")  #get('https://api.ipify.org').text


        # Finally we yield the all the data of a GPU as a dictionary
        yield response.meta.get('data')
