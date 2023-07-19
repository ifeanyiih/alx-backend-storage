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
    print(f'\tmethod GET: {nginx.find({"method": "GET"}).count_documents()}')
    print(f'\tmethod POST: {nginx.find({"method": "POST"}).count_documents()}')
    print(f'\tmethod PUT: {nginx.find({"method": "PUT"}).count_documents()}')
    print(f'\tmethod PATCH: '
          f'{nginx.find({"method": "PATCH"}).count_documents()}')
    print(f'\tmethod DELETE: '
          f'{nginx.find({"method": "DELETE"}).count_documents()}')
    print(
        f"{nginx.find({'method': 'GET', 'path': '/status'}).count_documents()}"
        f" status check")
    print("IPs:")
    ips = nginx.aggregate([{"$sortByCount": "$ip"}, {"$limit": 10}])
    for doc in ips:
        print(f'\t{doc.get("_id")}: {doc.get("count")}')


if __name__ == "__main__":
    printLog()
