/**
 * University Portal API Client
 * Type-safe API client connecting frontend to Django Ninja backend
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api';

// Type-safe fetch wrapper
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

// ============ CONFIG ============
export async function getConfig() {
  return fetchAPI<any>('/config');
}

// ============ UNIVERSITY ============
export async function getUniversities() {
  return fetchAPI<any[]>('/university/universities');
}

export async function getFaculties() {
  return fetchAPI<any[]>('/university/faculties');
}

export async function getDepartments() {
  return fetchAPI<any[]>('/university/departments');
}

export async function getProgrammes() {
  return fetchAPI<any[]>('/university/programmes');
}

// ============ ACADEMIC ============
export async function getCourses() {
  return fetchAPI<any[]>('/academic/courses');
}

export async function getCourse(id: string) {
  return fetchAPI<any>(`/academic/courses/${id}`);
}

export async function getEnrollments(studentId?: string) {
  const url = studentId 
    ? `/academic/enrollments?student_id=${studentId}`
    : '/academic/enrollments';
  return fetchAPI<any[]>(url);
}

// ============ STUDENTS ============
export async function getStudents() {
  return fetchAPI<any[]>('/students/students');
}

export async function getStudent(id: string) {
  return fetchAPI<any>(`/students/students/${id}`);
}

export async function getStudentByMatNo(matNo: string) {
  return fetchAPI<any>(`/students/students/by-matno/${matNo}`);
}

// ============ FINANCE ============
export async function getInvoices(studentId?: string) {
  const url = studentId
    ? `/finance/invoices?student_id=${studentId}`
    : '/finance/invoices';
  return fetchAPI<any[]>(url);
}

export async function getPayments(studentId?: string) {
  const url = studentId
    ? `/finance/payments?student_id=${studentId}`
    : '/finance/payments';
  return fetchAPI<any[]>(url);
}

export async function getFeeTypes() {
  return fetchAPI<any[]>('/finance/fee-types');
}

// ============ ADMISSION ============
export async function getAdmissionStats() {
  return fetchAPI<any>('/admission/statistics');
}

export async function getAdmissionApplications(status?: string) {
  const url = status
    ? `/admission/applications?status=${status}`
    : '/admission/applications';
  return fetchAPI<any[]>(url);
}

// ============ ATTENDANCE ============
export async function getAttendance(studentId?: string, courseId?: string) {
  let url = '/attendance/records';
  const params = new URLSearchParams();
  if (studentId) params.append('student_id', studentId);
  if (courseId) params.append('course_id', courseId);
  if (params.toString()) url += `?${params}`;
  return fetchAPI<any[]>(url);
}
