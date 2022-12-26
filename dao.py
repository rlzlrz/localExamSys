import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["lesdb"]
mycol = mydb["questions"]
userlist = mydb['users']