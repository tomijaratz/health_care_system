from app.helpers.helpers import json_contains_valid_entries

""" all the entries that a patient shall at least have"""
PATIENT_VALID_ENTRIES = {'identifier', 'active', 'name', 'telecom', 'gender',
                         'birthDate', 'deceasedBoolean', 'deceasedTime',
                         'address', 'maritalStatus', 'multipleBirthStatus',
                         'multipleBirthInteger', 'photo', 'contact', 'communication',
                         'multipleBirthBoolean', 'deceasedDateTime',
                         'generalPractitioner', 'managingOrganization', 'link',
                         'meta', 'implicitRules', 'language', 'text',
                         'contained', 'extension', 'modifierExtension', 'resourceType',
                         '_gender', '_birthDate', '_id',
                         }


def contact_contains_contact_details(contact):
    """

    :param contact: a patient contact
    :return: True if the contact has a any element to
    be referenced
    """
    return ('name' in contact
            or 'telecom' in contact
            or 'address' in contact
            or 'organization' in contact)


def patient_contacts_are_valid(patient_json):
    """

    :param patient_json: patient
    :return: True if the contacts in the patient are
    valid contacts, False if not
    """
    contacts = patient_json.get('contact')

    if contacts is not None:

        for contact in contacts:
            if not contact_contains_contact_details(contact):
                return False

    return True


def patient_provides_language(patient_json):
    if 'communication' in patient_json:
        for entry in patient_json.get('communication'):
            if 'language' not in entry:
                return False
    return True


def is_a_valid_patient(patient_json):
    """

    :param patient_json: a json representing a patient
    :return: result, errors_found, where result is a
    boolean representing the validity of the patient_json
    and errors is a list of the errors found in the document if
    there are any
    """
    validations = {}

    validations['invalid_contact_found'] = patient_contacts_are_valid(patient_json)
    validations['language_not_provided'] = patient_provides_language(patient_json)
    validations['invalid_entry_found'] = json_contains_valid_entries(patient_json, PATIENT_VALID_ENTRIES)

    result = True
    errors_found = []

    for validation, validation_result in validations.items():
        if not validation_result:
            result = False
            errors_found.append(validation)

    return result, errors_found
