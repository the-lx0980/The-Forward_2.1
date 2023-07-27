from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from config import Config

DATABASE_URI = "mongodb+srv://theprotullen:YHjSjKnLi8COtkZP@cluster0.eodxogb.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "forward_media" 
COLLECTION_NAME = "media-collection" 

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance(db)


@instance.register
class Data(Document):
    id = fields.StrField(attribute='_id')
    channel = fields.StrField()
    file_type = fields.StrField()
    message_id = fields.IntField()
    use = fields.StrField()
    caption = fields.StrField()

    class Meta:
        collection_name = COLLECTION_NAME

async def save_data(id, channel, message_id, caption, file_type):
    try:
        data = Data(
            id=id,
            use = "forward",
            channel=channel,
            message_id=message_id,
            caption=caption,
            file_type=file_type
        )
    except ValidationError:
        print('Error occurred while saving file in database')
    try:
        await data.commit()
    except DuplicateKeyError:
        print("Already saved in Database")
    else:
        try:
            print("Messsage saved in DB")
        except:
            pass

async def get_search_results():
    filter = {'use': "forward"}
    cursor = Data.find(filter)
    cursor.sort('$natural', -1)
    cursor.skip(0).limit(1)
    Messages = await cursor.to_list(length=1)
    return Messages

