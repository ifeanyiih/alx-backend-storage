#!/usr/bin/env python3
""" A  Python function that returns the list of school having
a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """Returns a list of documents having the same topic
    Args:
        mongo_collection (pymongo collection object)
        topic (str): topic
    Returns:
        list(dict)
    """
    result = mongo_collection.find({"topics": topic})
    return result
