""" controller and routes for patient """

import bson
from flask import request, jsonify
from app import app, mongo
from app.controllers import base_controller
from app.document_validators.patient_validator import is_a_valid_patient


@app.route('/patient/<id>', methods=['GET'])
def get_patient(id):
    return base_controller.get_document(mongo.db.patients, id)


@app.route('/patient', methods=['GET'])
def get_all_patients():
    return base_controller.get_all_documents(mongo.db.patients, 'patients')


@app.route('/patient/<id>/conditions', methods=['GET'])
def get_patient_conditions(id):
    """

    :param id: id of the patient
    :return: json list containing the conditions found for that patient
    """
    if bson.objectid.ObjectId.is_valid(id):
        return base_controller.get_all_documents_matching_filter(
            mongo.db.conditions, {"subject.reference": "Patient/" + str(id)})
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


@app.route('/patient', methods=['POST'])
def create_patient():
    return base_controller.create_document(mongo.db.patients, is_a_valid_patient)


@app.route('/patient/<id>', methods=['DELETE'])
def delete_patient(id):
    return base_controller.delete_document(mongo.db.patients, id)


@app.route('/patient', methods=['DELETE'])
def delete_all_patients():
    return base_controller.delete_all_documents(mongo.db.patients)


@app.route('/patient/<id>', methods=['PUT'])
def update_patient(id):
    patient_json = request.get_json()
    return base_controller.update_document(mongo.db.patients, id, patient_json, is_a_valid_patient)
