# pipelines.py
import psycopg2
from scrapy.exceptions import NotConfigured
from scrapy import signals

class PostgresPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = {
            'db': crawler.settings.get('POSTGRES_DB'),
            'user': crawler.settings.get('POSTGRES_USER'),
            'password': crawler.settings.get('POSTGRES_PASSWORD'),
            'host': crawler.settings.get('POSTGRES_HOST'),
            'port': crawler.settings.get('POSTGRES_PORT'),
        }
        if not all(db_settings.values()):
            raise NotConfigured('Database configuration is incomplete')

        pipeline = cls(db_settings)
        crawler.signals.connect(pipeline.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.connection = psycopg2.connect(**self.db_settings)
        self.cursor = self.connection.cursor()

    def spider_closed(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        insert_query = """
            INSERT INTO your_table_name (name, position, skills, linkedin_url)
            VALUES (%s, %s, %s, %s)
        """
        data = (item['Name'], item['Position'], item['Skills'], item['LinkedIn URL'])
        self.cursor.execute(insert_query, data)
        self.connection.commit()

        return item
