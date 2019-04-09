""" base controller for managing CRUD operations in mongoDb collections"""

from bson import ObjectId
from flask import request, jsonify

from app.helpers.helpers import is_a_valid_objectid


def get_document(collection, id):
    if is_a_valid_objectid(id):
        data = collection.find_one_or_404({'_id': ObjectId(id)})
        return jsonify(data), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


def get_all_documents(collection, collection_name):
    collection_items = collection.find({})
    return jsonify({collection_name: [element for element in collection_items]}), 200


def create_document(collection_to_insert_document_to, document_validation_function):
    data = request.get_json()
    if '_id' not in data:
        is_valid_document, errors = document_validation_function(data)
        if is_valid_document:

            ack = collection_to_insert_document_to.insert_one(data)
            return jsonify({'ok': True, 'message': 'document created successfully!', '_id': ack.inserted_id}), 201

        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!',
                            'errors_found': errors}), 400
    return jsonify({'ok': False, 'message': 'Bad request parameters!',
                    'error': '_id must not be present'}), 400


def delete_document(collection_to_delete_document_from, id):
    if is_a_valid_objectid(id):
        db_response = collection_to_delete_document_from.delete_one({'_id': ObjectId(id)})
        if db_response.deleted_count == 1:
            response = {'ok': True, 'message': 'record deleted'}
        else:
            response = {'ok': True, 'message': 'no record found'}
        return jsonify(response), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


def delete_all_documents(collection_to_empty):
    collection_to_empty.remove({})
    response = {'ok': True, 'message': 'records deleted'}
    return jsonify(response), 200


def update_document(collection_to_update_document, document_id, document_json, document_validation_function):
    if '_id' in document_json and document_json['_id'] == document_id:
        is_valid_document, errors = document_validation_function(document_json)
        if is_valid_document and is_a_valid_objectid(document_id):
            del document_json['_id']
            collection_to_update_document.replace_one({'_id': ObjectId(document_id)}, document_json, upsert=True)
            return jsonify({'ok': True, 'message': 'document updated successfully!', 'id': document_id}), 201
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!',
                            'errors_found': errors}), 400
    return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


def get_all_documents_matching_filter(collection, filter_criteria):
    """

    :param collection: a mongoDb collection, can't be null
    :param filter_criteria: a dictionary containing filter criteria for mongo
    :return: response with the list of documents found
    """
    data = collection.find(filter_criteria)
    return jsonify([condition for condition in data]), 200

