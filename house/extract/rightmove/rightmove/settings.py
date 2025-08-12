# Scrapy settings for rightmove project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from logging.handlers import TimedRotatingFileHandler
from scrapy.utils.log import configure_logging
import logging
from datetime import datetime
import os

current = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
logHandler = TimedRotatingFileHandler(
    f"logs/scrapyLog_{current}.log", when="midnight", interval=1
)
logHandler.setLevel(logging.INFO)
configure_logging(install_root_handler=False)
logging.basicConfig(handlers=[logHandler], level=logging.INFO)

BOT_NAME = "rightmove"

SPIDER_MODULES = ["rightmove.spiders"]
NEWSPIDER_MODULE = "rightmove.spiders"

ADDONS = {}

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# FEEDS = {
#     "s3://aws_key:aws_secret@quibbler-house-data-lake/%(name)s_batch_%(batch_time)s.csv": {
#         "format": "csv",
#         "encoding": "utf8",
#         "store_empty": False,
#         "fields": None,
#         "indent": 4,
#         "item_export_kwargs": {
#             "export_empty_fields": True,
#         },
#         "batch_item_count": 10000,
#     }
# }
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "rightmove (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,en-US;q=0.6",
    "Accept-Encoding": "gzip, deflate, zstd",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Host": "www.rightmove.co.uk",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
DOWNLOADER_MIDDLEWARES = {"scrapy_selenium.SeleniumMiddleware": 800}
SELENIUM_DRIVER_NAME = "firefox"
SELENIUM_DRIVER_EXECUTABLE_PATH = "C:\\Program Files\\geckodriver\\geckodriver.exe"
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #    "rightmove.middlewares.RightmoveDownloaderMiddleware": 2,
    # "scrapy_selenium.SeleniumMiddleware": 1,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     "rightmove.pipelines.RightmovePipeline": 1,
#     "rightmove.pipelines.UploadToS3Pipeline": 3,
#     "rightmove.pipelines.RemoveDuplicatesPipeline": 2,
# }

AWS_S3_BUCKET = "quibbler-house-data-lake"
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
