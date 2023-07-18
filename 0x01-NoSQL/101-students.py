#!/usr/bin/env python3
"""a Python function that returns all students sorted by average score"""


def top_students(mongo_collection):
    """Returns all students sorted by average score
    Args:
        mongo_collection (pymongo collection object)
    Returns:
        pymongo query
    """
    students = [dict(doc) for doc in mongo_collection.find({})]
    for student in students:
        av = sum([obj["score"] for obj in student["topics"]]) \
            / len(student["topics"])
        student["averageScore"] = av
    students.sort(key=lambda n: n["averageScore"], reverse=True)
    return students
