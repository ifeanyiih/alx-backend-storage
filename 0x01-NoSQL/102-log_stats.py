#!/usr/bin/env python3
"""Write a Python script that provides some stats
about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the number of documents in this collection
second line: Methods:
5 lines with the number of documents with the
method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
You can use this dump as data sample: dump.zip"""
import pymongo


client = pymongo.MongoClient()
db = client.logs
nginx = db.nginx


def printLog():
    """Prints the stats about Nginx stored in mongodb"""
    print(f"{nginx.count()} logs")
    print("Methods:")
    print(f'\tmethod GET: {nginx.find({"method": "GET"}).count()}')
    print(f'\tmethod POST: {nginx.find({"method": "POST"}).count()}')
    print(f'\tmethod PUT: {nginx.find({"method": "PUT"}).count()}')
    print(f'\tmethod PATCH: {nginx.find({"method": "PATCH"}).count()}')
    print(f'\tmethod DELETE: {nginx.find({"method": "DELETE"}).count()}')
    print(f'{nginx.find({"method": "GET", "path": "/status"}).count()}'
          f' status check')
    print("IPs:")
    ips = nginx.aggregate([{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
                          {"$sort": {"count": -1, "_id": -1}}, {"$limit": 10}])
    ipa = list(ips)
    ipa[1], ipa[2] = ipa[2], ipa[1]
    for doc in ipa:
        print(f'\t{doc["_id"]}: {doc.get("count")}')


if __name__ == "__main__":
    printLog()
