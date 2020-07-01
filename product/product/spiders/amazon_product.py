from scrapy import Spider,Request
from ..items import AmazonItem
import re


class AmazonProductSpider(Spider):

    name = "amazon_product"
    page_number = 1
    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    start_urls = [
        'https://www.amazon.in/s?k=watch&ref=nb_sb_noss',
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,callback=self.parse,headers=self.headers)

    def parse(self, response):
        watches = response.xpath("//a[@class='a-link-normal a-text-normal']/@href").extract()
        for watch in watches:
            watch_url = response.urljoin(watch)
            yield Request(url=watch_url,callback=self.parse_watches)

        if self.page_number <=10:
            print(self.page_number)
            self.page_number+=1
            next_page = response.xpath('//ul[@class="a-pagination"]/li[@class="a-last"]/a/@href').extract_first()
            next_page_url = response.urljoin(next_page)
            yield response.follow(url=next_page_url,callback=self.parse)

    def parse_watches(self, response):
        item = AmazonItem()
        item['product_brand'] = response.xpath("//a[@id='bylineInfo']//text()").get() or "Not Specified"
        item['product_brand'] = item['product_brand'].strip()

        item['product_name'] = response.xpath("//span[@id='productTitle']//text()").get() or response.xpath("//h1[@id='title']//text()").get()
        item['product_name'] = item['product_name'].strip()

        item['product_price'] = response.xpath("//span[@id='priceblock_ourprice']//text()").extract_first() or response.xpath("//span[@id='priceblock_dealprice']//text()").extract_first() or response.xpath("//span[@id='priceblock_saleprice']//text()").extract_first()
        item['product_price'] = item['product_price'].strip()
        item['product_price'] = re.findall("\d+\.\d+",item['product_price'])[0]

        item['product_availability'] = response.xpath("//div[@id='availability']").xpath("//span[@class='a-size-medium a-color-success']//text()").get() or "Out of stock"
        item['product_availability'] = item['product_availability'].strip()

        item['product_image'] = response.xpath("//img[@id='landingImage']/@data-old-hires").get() or response.xpath("//img[@id='imgBlkFront']/@src").get() or response.xpath("//div[@id='imgTagWrapperId']/img/@src")

        item['product_shipping'] = response.css('#price-shipping-message').xpath('//b//text()').extract_first() or "Not Available"
        item['product_shipping'] = item['product_shipping'].strip()

        features_dirty = response.xpath("//div[@id='featurebullets_feature_div']//span[@class='a-list-item']//text()").getall()
        features_clean = []
        for feature in features_dirty:
            features_clean.append(feature.strip())
        item['product_features'] = features_clean

        item['product_average_rating'] = response.css('#averageCustomerReviews').xpath('//i[@class="a-icon-alt"]//text()').extract_first() or "Not Available"
        item['product_average_rating'] = item['product_average_rating'].strip()

        yield item

        
