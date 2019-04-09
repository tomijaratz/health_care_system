""" controller and routes for condition """

from flask import request
from app import app, mongo
from app.controllers import base_controller
from app.document_validators.condition_validator import is_a_valid_condition


@app.route('/condition/<id>', methods=['GET'])
def get_condition(id):
    return base_controller.get_document(mongo.db.conditions, id)


@app.route('/condition', methods=['GET'])
def get_all_conditions():
    return base_controller.get_all_documents(mongo.db.conditions, 'conditions')


@app.route('/condition', methods=['POST'])
def create_condition():
    return base_controller.create_document(mongo.db.conditions, is_a_valid_condition)


@app.route('/condition/<id>', methods=['DELETE'])
def delete_condition(id):
    return base_controller.delete_document(mongo.db.conditions, id)


@app.route('/condition', methods=['DELETE'])
def delete_all_conditions():
    return base_controller.delete_all_documents(mongo.db.conditions)


@app.route('/condition/<id>', methods=['PUT'])
def update_condition(id):
    condition_json = request.get_json()
    return base_controller.update_document(mongo.db.conditions, id, condition_json, is_a_valid_condition)
