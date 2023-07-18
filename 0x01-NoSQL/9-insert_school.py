#!/usr/bin/env python3
""" A Python function that inserts a new document in a
collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection
    Args:
        mongo_collection (pymongo collection object)
    Returns:
        str : the id of the created document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
