import scrapy

class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/search?q=mobiles"]

    def start_requests(self):
        # Setting custom headers
        yield scrapy.Request(
            url=self.start_urls[0], 
            callback=self.parse,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.110 Safari/537.36'
            }
        )

    def parse(self, response):
        # Extracting product details
        products = response.xpath('//div[@class="_1AtVbE"]')
        for product in products:
            name = product.xpath('.//div[@class="_4rR01T"]/text()').get()
            specifications = product.xpath('.//ul[@class="_1xgFaf"]/li/text()').getall()

            ram = specifications[0] if len(specifications) > 0 else None
            display_size = specifications[1] if len(specifications) > 1 else None
            camera = specifications[2] if len(specifications) > 2 else None
            battery = specifications[3] if len(specifications) > 3 else None

            price = product.xpath('.//div[@class="_30jeq3 _1_WHN1"]/text()').get()

            yield {
                'name': name,
                'ram': ram,
                'display_size': display_size,
                'camera': camera,
                'battery': battery,
                'price': price
            }

        # Handling pagination
        next_page = response.xpath('//a[@class="_1LKTO3"][last()]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.110 Safari/537.36'
                }
            )


            


          

     
        
            
        
