from flask import Flask, request, jsonify

import db

app = Flask(__name__)


def handle_request(query_func: callable, is_json: bool = False, *args: any) -> tuple:
    """Handle requests by calling appropriate database functions and returning JSON response.

    Args:
        query_func (callable): Function to execute based on the request.
        is_json (bool, optional): Flag indicating if the data is in JSON format. Defaults to False.
        *args: Variable length argument list for passing to the query function.

    Returns:
        tuple: Tuple containing JSON response and status code.
    """
    success = query_func(*args) if not is_json else query_func(*args, request.json)
    if success:
        return jsonify({"message": "Success"}), 200
    return jsonify({"message": "Failed"}), 400


@app.route("/patients", methods=["GET"])
def get_patients() -> str:
    """Get all patients from the database.

    Returns:
        str: JSON response containing all patients.
    """
    patients = db.get_all_patients()
    return jsonify(patients)


@app.route("/patients", methods=["POST"])
def patients_requests() -> tuple:
    """Handle POST requests related to patients.

    Returns:
        tuple: Tuple containing JSON response and status code.
    """
    if request.method == "POST":
        return handle_request(db.add_patient, is_json=True)


@app.route("/patients/<patient_id>", methods=["DELETE", "PUT"])
def patients_id_requests(patient_id: str) -> tuple:
    """Handle DELETE and PUT requests related to individual patients.

    Args:
        patient_id (str): ID of the patient.

    Returns:
        tuple: Tuple containing JSON response and status code.
    """
    if request.method == "DELETE":
        return handle_request(db.delete_patient, False, patient_id)
    elif request.method == "PUT":
        return handle_request(db.update_patient, True, patient_id)


@app.route("/doctors", methods=["GET"])
def get_doctors() -> str:
    """Get all doctors from the database.

    Returns:
        str: JSON response containing all doctors.
    """
    doctors = db.get_all_doctors()
    return jsonify(doctors)


@app.route("/doctors", methods=["POST"])
def doctors_requests() -> tuple:
    """Handle POST requests related to doctors.

    Returns:
        tuple: Tuple containing JSON response and status code.
    """
    if request.method == "POST":
        return handle_request(db.add_doctor, is_json=True)


@app.route("/doctors/<doctor_id>", methods=["DELETE", "PUT"])
def doctors_id_requests(doctor_id: str) -> tuple:
    """Handle DELETE and PUT requests related to individual doctors.

    Args:
        doctor_id (str): ID of the doctor.

    Returns:
        tuple: Tuple containing JSON response and status code.
    """
    if request.method == "DELETE":
        return handle_request(db.delete_doctor, False, doctor_id)
    elif request.method == "PUT":
        return handle_request(db.update_doctor, True, doctor_id)


@app.route("/patients/all", methods=["GET"])
def get_patients_with_doctors_visits() -> str:
    """Get all patients with their doctors' visits from the database.

    Returns:
        str: JSON response containing patients with their doctors' visits.
    """
    patients = db.get_patients_with_doctors_visits()
    return jsonify(patients)


if __name__ == "__main__":
    app.run(debug=False)
