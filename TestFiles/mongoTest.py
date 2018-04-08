
from pymongo import MongoClient
import pprint
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import math
from keras import optimizers
from ast import literal_eval
from bson.objectid import ObjectId

client = MongoClient()
# get_database with no "name" argument chooses the DB from the URI
db = client.songDB
collection = db.tasks
#pprint.pprint(client.find_one())

lastPlayedList = list()
durationList = list()
bpmList = list()

locationList = list()
songNameList = list()

for obj in collection.find():
	#print(obj['songName'])
	
	lastPlayedList.append(obj['lastPlayed'])
	durationList.append(obj['duration'])
	bpmList.append(obj['bpm'])
	locationList.append(obj['locationName'])
	songNameList.append(obj['songName'])


 # now for the actual neural network stuff
 #
 #
 #
 #
 #
index_75 = math.ceil(len(durationList) * 0.75)
bpmList = bpmList[0:index_75]
durationList = durationList[0:index_75]








np.random.seed(7)




# creating the actual model model
model = Sequential()
model.add(Dense(12, input_dim= 1, activation='linear'))
model.add(Dense(8, activation='linear'))
model.add(Dense(1, activation='linear'))

# Compile model
sgd = optimizers.SGD(lr=0.00001, decay=1e-6, momentum=0.9, nesterov=True)

model.compile(loss='mean_squared_logarithmic_error', optimizer=sgd)



# Fit the model
# loss is about 0.12
# epochs is equal to the length of the items in the data
# batch size is 10 percent of this length
fullLength = int(len(lastPlayedList)/0.75)
model.fit(np.array(bpmList), np.array(durationList), epochs= fullLength, batch_size= int(fullLength * 0.10))

bpmListLast25 = bpmList[index_75: int(len(durationList))]
#durationListLast25 = durationList[index_75: int(len(durationList))]
predict = model.predict(np.array(bpmList))
NewPredict = np.array(predict)

songSet = set()

allSongsCollection =  db.allsongs
print("checking for songs")
for aPrediction in NewPredict:
	for obj in allSongsCollection.find():
		if int(obj['BPM'] ) in range(int(aPrediction[0]) -4, int(aPrediction[0]) + 4):
			songSet.add(obj['title'])
print(songSet)



#songList = ",".join(map(str, NewPredict))

setAsString = str(list(songSet))

aiCollection = db.aipredictions
if aiCollection.count() == 0:
	print("case 1")
	aiCollection.insert_one({'songList': list(songSet)})
else :
	print("case2")
	firstItem = aiCollection.find()
	first = firstItem[0]
	print(first['_id'])
	#aiCollection.find_one_and_update({"_id": first}, 
	#                             {"$set": {"songList": setAsString}})
	aiCollection.find_one_and_update({"_id": first}, {"$set": {'songList': list(songSet)}})
	#meSongs = {}
	#test = {'songList': songSet}
	#aiCollection.delete_many({'_id':ObjectId(first['_id'])})
	#aiCollection.insert_one({'songList': songSet})
	#aiCollection.update_one({'_id':ObjectId(first['_id'])}, {'$set': test}, upsert=False)

def setUpLists():
	
def predict():






