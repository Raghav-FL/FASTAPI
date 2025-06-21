def document_to_dict(doc):
    doc["_id"] = str(doc["_id"])
    return doc
