import React, { useState, useEffect } from 'react';
import { getDoctors, getAppointments } from '../api/client';
import CreateDoctorForm from '../components/CreateDoctorForm';
import CreateAppointmentForm from '../components/CreateAppointmentForm';

function Home() {
  const [doctors, setDoctors] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const doctorsRes = await getDoctors();
      setDoctors(doctorsRes.data.doctors);
      
      const appointmentsRes = await getAppointments();
      setAppointments(appointmentsRes.data.appointments);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={{padding: '20px'}}>Loading...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h1>Medical Appointment System Dashboard</h1>
      
      <div style={{ display: 'flex', gap: '20px' }}>
        <CreateDoctorForm onDoctorCreated={fetchData} />
        <CreateAppointmentForm onAppointmentCreated={fetchData} />
      </div>

      <div style={{ marginTop: '30px' }}>
        <h2>Doctors ({doctors.length})</h2>
        {doctors.length === 0 ? (
          <p>No doctors available</p>
        ) : (
          <ul>
            {doctors.map(doc => (
              <li key={doc.doctor_id}>
                <strong>{doc.first_name} {doc.last_name}</strong> - {doc.specialty}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div style={{ marginTop: '30px' }}>
        <h2>Appointments ({appointments.length})</h2>
        {appointments.length === 0 ? (
          <p>No appointments scheduled</p>
        ) : (
          <ul>
            {appointments.map(app => (
              <li key={app.appointment_id}>
                Patient {app.patient_id} with Doctor {app.doctor_id} - {app.appointment_time} <strong>({app.status})</strong>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Home;
