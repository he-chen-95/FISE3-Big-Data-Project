import numpy as np
from pymongo import MongoClient

def SaveAndFindResultById(results):
	uri = "mongodb://qc858020:OfCA37nkoyB4K1kFEYw4lVt1x5g4rQHAZeTw8UyIx04ulqqN7NxeH9jwI0YrYE9CcvnadmTn2YH6EOYyeFeuGA==@qc858020.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
	mongo_client = MongoClient(uri) 
	db = mongo_client.BigDataPj
	db.results.drop()

	length = results.size
	for i in range(0,length):
		row={}
		row['ID'] = i
		row['TARGET'] = int(results[i])
		db.results.insert_one(row)

	print('Search result by ID: 0 -',length-1,', -1 to exit')
	while(1):
		id = int(input())
		if(id == -1):
			print('Bye!')
			break
		elif(id >= 0 and id < length):
			query = {"ID":id}
			print(db.results.find_one(query)['TARGET'])
		else:
			print("ERROR!")