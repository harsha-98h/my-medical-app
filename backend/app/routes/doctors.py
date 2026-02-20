from flask import Blueprint, request, jsonify

bp = Blueprint('doctors', __name__, url_prefix='/api/v1/doctors')

doctors_db = {}
doctor_id_counter = 1

@bp.route('', methods=['POST'])
def create_doctor():
    global doctor_id_counter
    try:
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        specialty = data.get('specialty')
        
        if not all([first_name, last_name, specialty]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        doctor_id = doctor_id_counter
        doctor_id_counter += 1
        
        doctors_db[doctor_id] = {
            'first_name': first_name,
            'last_name': last_name,
            'specialty': specialty,
            'rating': 0,
            'created_at': str(__import__('datetime').datetime.now())
        }
        
        return jsonify({'message': 'Doctor created', 'doctor_id': doctor_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['GET'])
def get_doctors():
    try:
        doctors = []
        for doc_id, doc_data in doctors_db.items():
            doctor = {'doctor_id': doc_id, **doc_data}
            doctors.append(doctor)
        return jsonify({'doctors': doctors}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    try:
        if doctor_id not in doctors_db:
            return jsonify({'error': 'Doctor not found'}), 404
        
        doctor = {'doctor_id': doctor_id, **doctors_db[doctor_id]}
        return jsonify({'doctor': doctor}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
