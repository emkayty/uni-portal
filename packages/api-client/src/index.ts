// Auto-generated API types for University Portal
// Generated from Django Ninja API

// === CONFIG TYPES ===
export interface UniversityPreset {
  id: string;
  name: string;
  description: string;
  system_type: 'university' | 'polytechnic';
  academic_style: 'british_nigerian' | 'american';
  features: {
    grading: string;
    degree_duration: string;
    assessment: string;
    classifications: string[];
  };
}

export interface PresetsResponse {
  presets: UniversityPreset[];
}

// === UNIVERSITY TYPES ===
export interface University {
  id: string;
  name: string;
  code: string;
  type: string;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  established_year?: number;
  logo?: string;
}

export interface Faculty {
  id: string;
  name: string;
  code: string;
  university: string;
  dean?: string;
}

export interface Department {
  id: string;
  name: string;
  code: string;
  faculty: string;
  programme_type?: string;
}

export interface Session {
  id: string;
  name: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
}

export interface Semester {
  id: string;
  name: string;
  session: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
}

// === ACADEMIC TYPES ===
export interface Course {
  id: string;
  code: string;
  title: string;
  department?: string;
  level: number;
  units: number;
  semester?: string;
}

export interface Enrollment {
  id: string;
  student?: string;
  course?: string;
  semester?: string;
  status: string;
  enrolled_at?: string;
}

export interface Grade {
  id: string;
  student?: string;
  course?: string;
  score: number;
  grade: string;
  points: number;
  status: string;
}

export interface Timetable {
  id: string;
  course?: string;
  venue?: string;
  day: string;
  start_time: string;
  end_time: string;
}

export interface Venue {
  id: string;
  name: string;
  building: string;
  capacity: number;
  type: string;
}

export interface Hostel {
  id: string;
  name: string;
  gender: string;
  total_beds: number;
  occupied_beds: number;
  available: number;
}

export interface ExamSitting {
  id: string;
  course?: string;
  semester?: string;
  venue?: string;
  date: string;
  start_time: string;
  end_time: string;
}

// === FINANCE TYPES ===
export interface FeeType {
  id: string;
  name: string;
  category: string;
  amount: number;
  is_mandatory: boolean;
}

export interface Invoice {
  id: string;
  student?: string;
  semester?: string;
  amount: number;
  status: string;
  created_at?: string;
}

export interface Payment {
  id: string;
  student?: string;
  amount: number;
  method: string;
  status: string;
  date?: string;
}

export interface Installment {
  id: string;
  student?: string;
  amount: number;
  due_date?: string;
  status: string;
}

export interface Scholarship {
  id: string;
  name: string;
  amount: number;
  type: string;
  criteria?: string;
}

export interface ScholarshipApplication {
  id: string;
  student?: string;
  scholarship?: string;
  status: string;
  applied_at?: string;
}

// === STUDENT TYPES ===
export interface Student {
  id: string;
  matric_number?: string;
  name?: string;
  email?: string;
}

export interface StudentDocument {
  id: string;
  student?: string;
  document_type: string;
  status: string;
  uploaded_at?: string;
}

// === API CLIENT ===
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api';

class ApiClient {
  private baseUrl: string;
  
  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }
  
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
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
  
  // Config
  async getPresets(): Promise<PresetsResponse> {
    return this.request<PresetsResponse>('/config/presets');
  }
  
  // University
  async getUniversities(): Promise<University[]> {
    return this.request<University[]>('/university/universities');
  }
  
  async getFaculties(universityId?: string): Promise<Faculty[]> {
    const params = universityId ? `?university_id=${universityId}` : '';
    return this.request<Faculty[]>(`/university/faculties${params}`);
  }
  
  async getDepartments(facultyId?: string): Promise<Department[]> {
    const params = facultyId ? `?faculty_id=${facultyId}` : '';
    return this.request<Department[]>(`/university/departments${params}`);
  }
  
  async getSessions(): Promise<Session[]> {
    return this.request<Session[]>('/university/sessions');
  }
  
  async getSemesters(sessionId?: string): Promise<Semester[]> {
    const params = sessionId ? `?session_id=${sessionId}` : '';
    return this.request<Semester[]>(`/university/semesters${params}`);
  }
  
  // Academic
  async getCourses(params?: { department_id?: string; level?: number; semester?: string }): Promise<Course[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Course[]>(`/academic/courses${query ? `?${query}` : ''}`);
  }
  
  async getEnrollments(params?: { student_id?: string; course_id?: string; semester_id?: string }): Promise<Enrollment[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Enrollment[]>(`/academic/enrollments${query ? `?${query}` : ''}`);
  }
  
  async getGrades(params?: { student_id?: string; course_id?: string; semester_id?: string }): Promise<Grade[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Grade[]>(`/academic/grades${query ? `?${query}` : ''}`);
  }
  
  async getTimetables(params?: { course_id?: string; semester_id?: string; day?: string }): Promise<Timetable[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Timetable[]>(`/academic/timetables${query ? `?${query}` : ''}`);
  }
  
  async getVenues(params?: { building?: string; capacity?: number }): Promise<Venue[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Venue[]>(`/academic/venues${query ? `?${query}` : ''}`);
  }
  
  async getHostels(params?: { university_id?: string; gender?: string }): Promise<Hostel[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Hostel[]>(`/academic/hostels${query ? `?${query}` : ''}`);
  }
  
  async getExams(params?: { course_id?: string; semester_id?: string; date?: string }): Promise<ExamSitting[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<ExamSitting[]>(`/academic/exams${query ? `?${query}` : ''}`);
  }
  
  // Finance
  async getFeeTypes(params?: { university_id?: string; category?: string }): Promise<FeeType[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<FeeType[]>(`/finance/fee-types${query ? `?${query}` : ''}`);
  }
  
  async getInvoices(params?: { student_id?: string; semester_id?: string; status?: string }): Promise<Invoice[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Invoice[]>(`/finance/invoices${query ? `?${query}` : ''}`);
  }
  
  async getPayments(params?: { student_id?: string; invoice_id?: string; status?: string }): Promise<Payment[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Payment[]>(`/finance/payments${query ? `?${query}` : ''}`);
  }
  
  async getInstallments(params?: { student_id?: string; status?: string }): Promise<Installment[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Installment[]>(`/finance/installments${query ? `?${query}` : ''}`);
  }
  
  async getScholarships(params?: { university_id?: string; scholarship_type?: string; status?: string }): Promise<Scholarship[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Scholarship[]>(`/finance/scholarships${query ? `?${query}` : ''}`);
  }
  
  async getScholarshipApplications(params?: { student_id?: string; scholarship_id?: string; status?: string }): Promise<ScholarshipApplication[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<ScholarshipApplication[]>(`/finance/scholarship-applications${query ? `?${query}` : ''}`);
  }
  
  // Students
  async getStudents(params?: { department_id?: string; level?: number }): Promise<Student[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<Student[]>(`/students/students${query ? `?${query}` : ''}`);
  }
  
  async getDocuments(params?: { student_id?: string; document_type?: string }): Promise<StudentDocument[]> {
    const query = new URLSearchParams(params as Record<string, string>).toString();
    return this.request<StudentDocument[]>(`/students/documents${query ? `?${query}` : ''}`);
  }
}

// Export singleton instance
export const api = new ApiClient();

// Export types for consumption
export type {
  UniversityPreset,
  PresetsResponse,
  University,
  Faculty,
  Department,
  Session,
  Semester,
  Course,
  Enrollment,
  Grade,
  Timetable,
  Venue,
  Hostel,
  ExamSitting,
  FeeType,
  Invoice,
  Payment,
  Installment,
  Scholarship,
  ScholarshipApplication,
  Student,
  StudentDocument,
};

// === AUTH TYPES ===
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  student_id?: string;
  role?: string;
}

export interface UserResponse {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  student_id?: string;
  is_active: boolean;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: UserResponse;
}

// === ACADEMIC NEW TYPES ===
export interface CourseRegistrationRequest {
  student_id: string;
  semester_id: string;
  course_ids: string[];
}

export interface GradeSubmissionRequest {
  enrollment_id: string;
  ca_score: number;
  exam_score: number;
}

export interface AttendanceRecord {
  student_id: string;
  course_id: string;
  date: string;
  status: string;
}

export interface DegreeAudit {
  student_id: string;
  degree: string;
  total_required: number;
  units_earned: number;
  units_remaining: number;
  gpa: number;
  graduation_eligible: boolean;
  completed_courses: any[];
  missing_courses: string[];
  progress_percent: number;
}

// === FINANCE NEW TYPES ===
export interface PaymentRequest {
  student_id: string;
  invoice_id: string;
  amount: number;
  payment_method: string;
}

export interface HostelApplicationRequest {
  student_id: string;
  hostel_id: string;
  room_type: string;
  semester_id: string;
}

export interface TranscriptRequest {
  student_id: string;
  transcript_type: string;
  delivery_method: string;
}

export interface NotificationRequest {
  recipient_id: string;
  channel: string;
  subject?: string;
  message: string;
  priority?: string;
}

// === EXTENDED API CLIENT ===
export class ExtendedApiClient extends ApiClient {
  // Auth
  async login(data: LoginRequest): Promise<TokenResponse> {
    return this.request<TokenResponse>('/auth/login', { method: 'POST', body: JSON.stringify(data) });
  }

  async register(data: RegisterRequest): Promise<TokenResponse> {
    return this.request<TokenResponse>('/auth/register', { method: 'POST', body: JSON.stringify(data) });
  }

  async getCurrentUser(headers?: HeadersInit): Promise<UserResponse> {
    return this.request<UserResponse>('/auth/me', { headers });
  }

  async getRoles(): Promise<any> {
    return this.request('/auth/roles');
  }

  async getPermissions(role: string): Promise<any> {
    return this.request(`/auth/permissions/${role}`);
  }

  // Academic - New
  async registerCourses(data: CourseRegistrationRequest): Promise<any> {
    return this.request('/academic/enrollments/register', { method: 'POST', body: JSON.stringify(data) });
  }

  async submitGrade(data: GradeSubmissionRequest): Promise<any> {
    return this.request('/academic/grades/submit', { method: 'POST', body: JSON.stringify(data) });
  }

  async calculateGPA(studentId: string): Promise<any> {
    return this.request(`/academic/grades/calculate-gpa/${studentId}`);
  }

  async markAttendance(data: AttendanceRecord): Promise<any> {
    return this.request('/academic/attendance/mark', { method: 'POST', body: JSON.stringify(data) });
  }

  async getAttendance(studentId: string): Promise<any> {
    return this.request(`/academic/attendance/${studentId}`);
  }

  async getAttendanceSummary(studentId: string): Promise<any> {
    return this.request(`/academic/attendance/${studentId}/summary`);
  }

  async getDegreeAudit(studentId: string): Promise<DegreeAudit> {
    return this.request(`/academic/degree-audit/${studentId}`);
  }

  // Finance - New
  async initiatePayment(data: PaymentRequest): Promise<any> {
    return this.request('/finance/payments/initiate', { method: 'POST', body: JSON.stringify(data) });
  }

  async verifyPayment(transactionId: string): Promise<any> {
    return this.request(`/finance/payments/${transactionId}/verify`, { method: 'POST' });
  }

  async applyForHostel(data: HostelApplicationRequest): Promise<any> {
    return this.request('/finance/hostel/apply', { method: 'POST', body: JSON.stringify(data) });
  }

  async getHostelApplications(studentId: string): Promise<any> {
    return this.request(`/finance/hostel/applications/student/${studentId}`);
  }

  async requestTranscript(data: TranscriptRequest): Promise<any> {
    return this.request('/finance/transcript/request', { method: 'POST', body: JSON.stringify(data) });
  }

  async getTranscriptRequests(studentId: string): Promise<any> {
    return this.request(`/finance/transcript/requests/student/${studentId}`);
  }

  async sendNotification(data: NotificationRequest): Promise<any> {
    return this.request('/finance/notifications/send', { method: 'POST', body: JSON.stringify(data) });
  }

  async getNotifications(studentId: string): Promise<any> {
    return this.request(`/finance/notifications/student/${studentId}`);
  }

  async sendBulkNotification(recipientIds: string[], channel: string, message: string): Promise<any> {
    return this.request('/finance/notifications/bulk', { 
      method: 'POST', 
      body: JSON.stringify({ recipient_ids: recipientIds, channel, message }) 
    });
  }

  async getRealtimeConfig(): Promise<any> {
    return this.request('/finance/realtime/config');
  }
}

export const extendedApi = new ExtendedApiClient();