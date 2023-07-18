#!/usr/bin/env python3
"""A Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """Lists all documents of a collection
    Args:
        mongo_collection (pymongo collection object)
    """
    documents = mongo_collection.find({})
    return documents
