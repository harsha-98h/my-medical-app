from flask import Blueprint, request, jsonify

bp = Blueprint('patients', __name__, url_prefix='/api/v1/patients')

patients_db = {}
patient_id_counter = 1

@bp.route('', methods=['POST'])
def create_patient():
    global patient_id_counter
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        
        if not all([first_name, last_name, phone]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        patient_id = patient_id_counter
        patient_id_counter += 1
        
        patients_db[patient_id] = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'created_at': str(__import__('datetime').datetime.now())
        }
        
        return jsonify({'message': 'Patient created', 'patient_id': patient_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['GET'])
def get_patients():
    try:
        patients = []
        for pat_id, pat_data in patients_db.items():
            patient = {'patient_id': pat_id, **pat_data}
            patients.append(patient)
        return jsonify({'patients': patients}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        if patient_id not in patients_db:
            return jsonify({'error': 'Patient not found'}), 404
        
        patient = {'patient_id': patient_id, **patients_db[patient_id]}
        return jsonify({'patient': patient}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
