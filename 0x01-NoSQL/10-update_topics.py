#!/usr/bin/env python3
""" A Python function that changes all topics of a school
document based on the name"""


def update_topics(mongo_collection, name, topics):
    """Updates the topics of a school, based on
    the document name
    Args:
        (mongo_collection): pymongo collection obj
        name (str): name
        topics (list[str]): a list of topics
    Returns:
        None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
