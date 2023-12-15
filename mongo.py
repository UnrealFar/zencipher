from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Document, fields, validate
from umongo.frameworks import MotorAsyncIOInstance
import bson
import os
import utils
import bcrypt



client = AsyncIOMotorClient(os.environ['MONGO_URI'])
db = client["DB"]

instance = MotorAsyncIOInstance()
instance.set_db(db)


async def create_user(username, password, email):
    uid = bson.ObjectId()
    salt = bcrypt.gensalt()
    hashed = utils.hash_password(password, salt)
    _key = utils.key_from_password(hashed, salt)
    user = User(
        _id=uid,
        username=username.lower(),
        password=hashed,
        salt=salt.decode(),
        email=utils.encrypt(email, _key),
        verified=True,
        plan=0,
    )
    await user.commit()
    return user

async def get_user(**kwargs):
    return await User.find_one(kwargs)

@instance.register
class User(Document):
    _id = fields.ObjectIdField(unique=True)
    username = fields.StrField(
        validate=validate.Length(max=50), required=True, unique=True
    )
    password = fields.StrField(required=True)
    salt = fields.StrField(required=True)
    email = fields.StrField(required=True)
    verified = fields.BooleanField(required=True)
    plan = fields.IntegerField()

    @property
    def key(self) -> str:
        return utils.key_from_password(self.password, self.salt.encode())

    async def new_password(
        self,
        title,
        username,
        password,
        note = None
    ):
        key = self.key
        p = Password(
            owner = self,
            title = title,
            username = utils.encrypt(username, key),
            password = utils.encrypt(password, key),
            note = note
        )
        await p.commit()
        return p

    async def passwords(self):
        ret = []
        async for i in Password.find({"owner":self}):
            ret.append({
                "title": i.title,
                "username": utils.decrypt(i.username, self.key),
                "password": utils.decrypt(i.password, self.key),
                "note": i.note
            })
        return ret

@instance.register
class Password(Document):
    owner = fields.ReferenceField("User", required=True)
    title = fields.StrField(required=True, unique=True)
    username = fields.StrField(required=True)
    password = fields.StrField(required=True)
    note = fields.StrField(required=False, default=None)
