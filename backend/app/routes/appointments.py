from flask import Blueprint, request, jsonify

bp = Blueprint('appointments', __name__, url_prefix='/api/v1/appointments')

appointments_db = {}
appointment_id_counter = 1

@bp.route('', methods=['POST'])
def create_appointment():
    global appointment_id_counter
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        appointment_time = data.get('appointment_time')
        
        if not all([patient_id, doctor_id, appointment_time]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        appointment_id = appointment_id_counter
        appointment_id_counter += 1
        
        appointments_db[appointment_id] = {
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'appointment_time': appointment_time,
            'status': 'scheduled',
            'created_at': str(__import__('datetime').datetime.now())
        }
        
        return jsonify({'message': 'Appointment created', 'appointment_id': appointment_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['GET'])
def get_appointments():
    try:
        appointments = []
        for app_id, app_data in appointments_db.items():
            appointment = {'appointment_id': app_id, **app_data}
            appointments.append(appointment)
        return jsonify({'appointments': appointments}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    try:
        if appointment_id not in appointments_db:
            return jsonify({'error': 'Appointment not found'}), 404
        
        appointment = {'appointment_id': appointment_id, **appointments_db[appointment_id]}
        return jsonify({'appointment': appointment}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        if appointment_id not in appointments_db:
            return jsonify({'error': 'Appointment not found'}), 404
        
        data = request.get_json()
        status = data.get('status')
        
        if status:
            appointments_db[appointment_id]['status'] = status
        
        return jsonify({'message': 'Appointment updated', 'appointment_id': appointment_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        if appointment_id not in appointments_db:
            return jsonify({'error': 'Appointment not found'}), 404
        
        del appointments_db[appointment_id]
        return jsonify({'message': 'Appointment deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
