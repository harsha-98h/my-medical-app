import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Auth
export const registerUser = (email, password, role) =>
  apiClient.post('/auth/register', { email, password, role });

export const loginUser = (email, password) =>
  apiClient.post('/auth/login', { email, password });

// Doctors
export const getDoctors = () =>
  apiClient.get('/doctors');

export const getDoctor = (id) =>
  apiClient.get(`/doctors/${id}`);

export const createDoctor = (data) =>
  apiClient.post('/doctors', data);

// Patients
export const getPatients = () =>
  apiClient.get('/patients');

export const getPatient = (id) =>
  apiClient.get(`/patients/${id}`);

export const createPatient = (data) =>
  apiClient.post('/patients', data);

// Appointments
export const getAppointments = () =>
  apiClient.get('/appointments');

export const getAppointment = (id) =>
  apiClient.get(`/appointments/${id}`);

export const createAppointment = (data) =>
  apiClient.post('/appointments', data);

export const updateAppointment = (id, data) =>
  apiClient.put(`/appointments/${id}`, data);

export const deleteAppointment = (id) =>
  apiClient.delete(`/appointments/${id}`);
