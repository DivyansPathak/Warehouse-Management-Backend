from typing import Any


def serialize_document(document: dict | None) -> dict | None:
    if document is None:
        return None

    document["_id"] = str(document["_id"])

    return document


def serialize_documents(documents: list[dict]) -> list[dict]:
    return [serialize_document(document) for document in documents]