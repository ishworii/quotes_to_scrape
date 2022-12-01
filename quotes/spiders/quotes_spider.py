import scrapy


class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        all_quotes = response.css(".quote")
        for quote in all_quotes:
            quote_text = quote.css("span.text::text").get()
            author_name = quote.css("span small.author::text").get()
            author_page = quote.css("span a::attr(href)").get()
            tags = quote.css(".tags meta.keywords::attr(content)").get()

            yield {
                "quote": quote_text,
                "author_name": author_name,
                "author_page": author_page,
                "tags": tags,
            }
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
