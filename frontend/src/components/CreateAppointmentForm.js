import React, { useState } from 'react';
import { createAppointment } from '../api/client';

function CreateAppointmentForm({ onAppointmentCreated }) {
  const [patientId, setPatientId] = useState('');
  const [doctorId, setDoctorId] = useState('');
  const [appointmentTime, setAppointmentTime] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      await createAppointment({ 
        patient_id: parseInt(patientId), 
        doctor_id: parseInt(doctorId), 
        appointment_time: appointmentTime 
      });
      setSuccess('Appointment created successfully!');
      setPatientId('');
      setDoctorId('');
      setAppointmentTime('');
      setTimeout(() => {
        setSuccess('');
        onAppointmentCreated();
      }, 2000);
    } catch (err) {
      setError('Failed to create appointment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>Create Appointment</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>Patient ID:</label>
          <input
            type="number"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>Doctor ID:</label>
          <input
            type="number"
            value={doctorId}
            onChange={(e) => setDoctorId(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>Appointment Time:</label>
          <input
            type="datetime-local"
            value={appointmentTime}
            onChange={(e) => setAppointmentTime(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{ width: '100%', padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          {loading ? 'Creating...' : 'Create Appointment'}
        </button>
      </form>
    </div>
  );
}

export default CreateAppointmentForm;
