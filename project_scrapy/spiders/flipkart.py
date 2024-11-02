import scrapy

class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["www.flipkart.com"]
    start_urls = ["https://www.flipkart.com/search?q=mobiles"]

    def start_requests(self):
        # Setting custom headers
        yield scrapy.Request(
            url='https://www.flipkart.com/search?q=mobiles', 
            callback=self.parse,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.110 Safari/537.36'
            }
        )

    def parse(self, response):

        products = response.xpath('//div[contains(@class,"yKfJKb row")]')
        for product in products:
            name = product.xpath('.//div[contains(@class,"KzDlHZ")]/text()').get()
            specifications = product.xpath('.//ul[contains(@class,"G4BRas")]/li')

            # Safely accessing each specification if available
            ram = specifications[0].xpath('.//text()').get() if len(specifications) > 1 else None
            display_size = specifications[2].xpath('.//text()').get() if len(specifications) > 2 else None
            camera = specifications[3].xpath('.//text()').get() if len(specifications) > 3 else None
            battery = specifications[4].xpath('.//text()').get() if len(specifications) > 4 else None
            processor = specifications[5].xpath('.//text()').get() if len(specifications) > 5 else None
            
            price = product.xpath('.//div[contains(@class,"Nx9bqj _4b5DiR")]/text()').get()

            yield {
                'name': name,
                'ram': ram,
                'display_size': display_size,
                'camera': camera,
                'battery': battery,
                'price': price,
                'processor':processor
            }

        second_page=response.xpath('//a[contains(@class,"cn++Ap")][2]/@href').get()
        second_page_url=response.urljoin(second_page)
        if second_page:
            yield response.follow(url=second_page_url,callback=self.parse)
        url=response.xpath('//a[contains(@class,"_9QVEpD")][2]/@href').get()
        next_page_url=response.urljoin(url)
        if next_page_url:
            yield response.follow(url=next_page_url,callback=self.parse)
            


          

     
        
            
        
