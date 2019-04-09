import bson
from bson import ObjectId
import re
from app import mongo
from app.helpers.helpers import json_contains_valid_entries

""" all the entries that a condition shall at least have"""
CONDITION_VALID_ENTRIES = {'identifier', 'clinicalStatus', 'verificationStatus',
                           'category', 'severity', 'code', 'bodySite', 'subject',
                           'encounter', 'onsetDateTime', 'onsetAge', 'onsetRange',
                           'onsetString', 'abatementDateTime', 'abatementAge',
                           'abatementPeriod', 'abatementRange', 'abatementString',
                           'recordedDate', 'recorder', 'asserter', 'stage', 'evidence',
                           'note', 'meta', 'implicitRules', 'language', 'text',
                           'contained', 'extension', 'modifierExtension', 'resourceType', '_id'
                           }

VERIFICATION_SATUS_ERROR_CODE = 'entered-in-error'
VERIFICATION_SATUS_ERROR_SYSTEM = 'http://terminology.hl7.org/CodeSystem/condition-ver-status'


def stage_is_valid(condition_json):
    """

    :param condition_json: the condition
    :return: True when the stage is valid, false when it is not.
    """
    if 'stage' not in condition_json:
        return True

    for stage in condition_json.get('stage'):
        if 'summary' not in stage and 'assessment' not in stage:
            return False

    return True


def clinical_status_not_present_when_verification_status_in_error(condition_json):
    """

    :param condition_json: the condition
    :return: True when clinicalStatus is empty, false if it is not empty
    and a verificationStatus entry represents an entered-in-error status
    """
    if 'clinicalStatus' in condition_json:
        # an empty dictionary evaluates to False in python
        if bool(condition_json.get('clinicalStatus')):
            error_entries = filter(filter_by_error_code, condition_json.get('verificationStatus').get('coding'))

            if len(list(error_entries)) > 0:
                return False
            else:
                return True

    return True


def evidence_is_valid(condition_json):
    """

    :param condition_json: the condition
    :return: True when the evidence in the condition is consistent
    with the FHIR standard
    """
    if 'evidence' not in condition_json:
        return True

    for evidence in condition_json.get('evidence'):
        if 'code' not in evidence and 'details' not in evidence:
            return False

    return True


def reference_subject_is_present(condition_json):
    """

    :param condition_json: the condition
    :return: True if the condition has a subject reference, False if not
    """
    if 'subject' in condition_json:
        if 'reference' in condition_json.get('subject'):
            return True
    return False


def patient_reference_is_present(condition_json):
    """

    :param condition_json: the condition
    :return: True if the condition is associated to a patient
    present in the system, if the id provided is not a valid
    ObjectId or no patient is found with that id False is returned.
    """
    if reference_subject_is_present(condition_json):
        reference_subject = condition_json.get('subject').get('reference')
        try:
            patient_reference_id = re.search('Patient/(.+)', reference_subject).group(1)
            if bson.objectid.ObjectId.is_valid(patient_reference_id):
                patient_present = mongo.db.patients.find_one({'_id': ObjectId(patient_reference_id)})
                if patient_present:
                    return True
        except AttributeError:
            return False

    return False


def is_a_valid_condition(condition_json):
    """

    :param condition_json: a json representing a condition
    :return: result, errors_found, where result is a
    boolean representing the validity of the condition_json
    and errors is a list of the errors found in the document if
    there are any
    """
    validations = {}

    validations['reference_patient_not_found'] = patient_reference_is_present(condition_json)
    validations['missing_reference_subject'] = reference_subject_is_present(condition_json)
    validations['invalid_stage'] = stage_is_valid(condition_json)
    validations['invalid_evidence_found'] = evidence_is_valid(condition_json)
    validations['clinical_status_not_empty_when_verification_status_with_error'] = \
        clinical_status_not_present_when_verification_status_in_error(
            condition_json)
    validations['invalid_entry_found'] = json_contains_valid_entries(condition_json, CONDITION_VALID_ENTRIES)

    result = True
    errors_found = []

    for validation, validation_result in validations.items():
        if not validation_result:
            result = False
            errors_found.append(validation)

    return result, errors_found


def filter_by_error_code(coding_entry):
    """

    :param coding_entry: condition coding
    :return: true if the coding entry represents a
    'entered-in-error' status
    """
    if coding_entry.get('system') == VERIFICATION_SATUS_ERROR_SYSTEM and \
            coding_entry.get('code') == VERIFICATION_SATUS_ERROR_CODE:
        return True
    return False
