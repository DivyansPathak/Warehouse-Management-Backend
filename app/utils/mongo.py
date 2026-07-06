from datetime import datetime
from typing import Any

from bson import ObjectId


def serialize_document(document: dict | None) -> dict | None:
    if document is None:
        return None

    document["_id"] = str(document["_id"])

    return document


def serialize_documents(documents: list[dict]) -> list[dict]:
    return [serialize_document(document) for document in documents]


def serialize_dashboard_document(document: dict | None) -> dict | None:
    if document is None:
        return None

    data = {}

    for key, value in document.items():

        if key == "_id":
            data["id"] = str(value)

        elif isinstance(value, ObjectId):
            data[key] = str(value)

        elif isinstance(value, datetime):
            data[key] = value.isoformat()

        else:
            data[key] = value

    return data


def serialize_dashboard_documents(
    documents: list[dict],
) -> list[dict]:
    return [
        serialize_dashboard_document(document)
        for document in documents
    ]