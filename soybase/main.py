from scrapy.cmdline import execute
from soybase.pipelines import SoybasePipeline

if __name__ == '__main__':
    soypipline = SoybasePipeline()
    info = soypipline.create_table()
    print(info)
    execute("scrapy crawl soybase".split())