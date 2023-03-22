from flask import Flask, render_template, request
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["chat_database"]

l2 = list(db.messages.find({}))
#print(l2)

l1 = list(db.messages.find({}, {'_id': 0, 'message': 1}))
#print(l1)

message = "hello world"
db.messages.insert_one({"message": message})
print("done")

messages = []
#for doc in db.messages.find({}, {'_id': 0, 'message': 1}):
#    messages.append(doc['message'])

print(messages)
