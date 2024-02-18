# middlewares.py

from scrapy import signals

class YourProjectNameMiddleware:
    def process_request(self, request, spider):
        # Add a custom header to each request
        request.headers['User-Agent'] = 'Your Custom User-Agent'

    def process_response(self, request, response, spider):
        # Process the response if needed
        return response

    def process_exception(self, request, exception, spider):
        # Handle exceptions if needed
        pass

# Attach the middleware to signals
class YourProjectNameMiddlewareManager:
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        spider.signals.connect(self.process_spider_input, signal=signals.spider_input)
        spider.signals.connect(self.process_spider_output, signal=signals.spider_output)
        spider.signals.connect(self.process_spider_exception, signal=signals.spider_exception)
        spider.signals.connect(self.process_spider_closed, signal=signals.spider_closed)

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_spider_closed(self, reason, spider):
        pass
