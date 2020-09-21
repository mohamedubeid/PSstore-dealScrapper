
BOT_NAME = 'psspider'
ITEM_PIPELINES = {'psspider.pipelines.MongoDbPipeline' : 300, }
SPIDER_MODULES = ['psspider.spiders']
NEWSPIDER_MODULE = 'psspider.spiders'
MONGO_URI = "mongodb+srv://OdyHayek:FLyme2themoo@simple.4x8wc.mongodb.net/Telegrambotps?retryWrites=true&w=majority"
MONGO_DATABASE = "Telegrambotps"
MONGODB_COLLECTION ='psSales'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


#DOWNLOAD_DELAY = 3

