import bson


def json_contains_valid_entries(json_document, valid_entries):
    """

    :param json_document: json to verify entries, can't be null
    :param valid_entries: a list of valid entries
    :return: True if every first level key in the json_document
    belongs to valid_entries
    """
    for key in json_document.keys():
        if key not in valid_entries:
            return False
    return True


def is_a_valid_objectid(id):
    """

    :param id: can't be null
    :return: True if 'id' is a valid objectId, False if not
    """
    return bson.objectid.ObjectId.is_valid(id)
