import logging
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from config import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DATABASE_URI = "mongodb+srv://theprotullen:YHjSjKnLi8COtkZP@cluster0.eodxogb.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "forward_media" 
COLLECTION_NAME = "media-collection" 


client = AsyncIOMotorClient(DATABASE_URI)
database = client[DATABASE_NAME]
instance = Instance.from_db(database)

@instance.register
class Data(Document):
    id = fields.StrField(attribute='_id')
 #   id_s = fields.StrField(required=True)
    channel = fields.StrField(required=True)
    file_type = fields.StrField(required=True)
    message_id = fields.IntField(required=True)
    use = fields.StrField(required=True)
    caption = fields.StrField(required=True)

    class Meta:
        collection_name = COLLECTION_NAME

async def save_data(id, channel, message_id, caption, file_type):
  #  id = file_id
    try:
        data = Data(
            id=id,
         #   id_s=file_id,
            use = "forward",
            channel=channel,
            message_id=message_id,
            caption=caption,
            file_type=file_type
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in database')
    try:
        await data.commit()
    except DuplicateKeyError:
        logger.warning("Already saved in Database")
    else:
        try:
            logger.info("Messsage saved in DB")
        except:
            pass

async def get_search_results():
    filter = {'use': "forward"}
    cursor = Data.find(filter)
    cursor.sort('$natural', 1)
    cursor.skip(0).limit(1)
    Messages = await cursor.to_list(length=1)
    return Messages

