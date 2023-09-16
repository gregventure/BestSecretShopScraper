import logging
import json

from BestSecretShop.storage.blobstorage import AzureBlobStorage
from BestSecretShop.storage.database import MySQLCataloguePageFullShopStore

from BestSecretShop.settings import CATALOGUE_PAGE_FULL_SHOP_LOCALPATH
from BestSecretShop.settings import CATALOGUE_PAGE_FULL_SHOP_DEST_BLOB


class SaveToMySQLPipeline_CataloguePageFullShop(MySQLCataloguePageFullShopStore):

    def __init__(self):
        super().__init__()

    def process_item(self, item, spider):
        self.upload_item(item)
        return item

    def close_spider(self, spider):
        self.close_database()


class UploadToBlobStorage_CataloguePageFullShop():

    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)
        self.container = 'product-gtin'
        
    def close_spider(self, spider):
        db = MySQLCataloguePageFullShopStore()
        table = db.get_table_V2()
        db.close_database()

        del table["id"]
        table.replace({0: False, 1: True}, inplace=True)
        table['crawl_date'] = table['crawl_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        object = table.to_dict(orient="records")
        
        with open(CATALOGUE_PAGE_FULL_SHOP_LOCALPATH, "w") as fp:
            fp.write(json.dumps(object, ensure_ascii=False))

        AzureBlobStorage.upload_file_to_blobstorage(
            self.container,
            CATALOGUE_PAGE_FULL_SHOP_DEST_BLOB,
            CATALOGUE_PAGE_FULL_SHOP_LOCALPATH
            )
        self.logger.info('Upload Products to BestSecretBlobStorage.')