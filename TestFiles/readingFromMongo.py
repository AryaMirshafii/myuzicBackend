from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId
import pprint

#client = MongoClient('mongodb://localhost:3000/tasks')
client = MongoClient()
#client = MongoClient('local', 27017)

#client = MongoClient('http://192.168.0.5:3000/tasks/')
#db = client.primer

#coll = db.dataset
print("HI")
#print(coll)

def get(post_id):
    # Convert from string to ObjectId:
    document = client.db.collection.find_one({'_id': ObjectId(post_id)})
    print("here")
    print(document)

#db = client.Tasks
#get('5a3eb23baa26ec6114918249')





# The web framework gets post_id from the URL and passes it as a string

db = client.Tododb
cursor = db.find({})
for document in cursor: 
    pprint(document)
