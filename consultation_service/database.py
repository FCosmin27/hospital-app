from mongoengine import connect
from config import MONGODB_URI

connect(host=MONGODB_URI)