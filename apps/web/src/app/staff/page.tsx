"use client";
import { useState } from "react";
import { Users, Search, Mail, Phone, Book, Award } from "lucide-react";

const staff = [
  { id: 1, name: "Dr. Adebayo", title: "Professor", department: "Computer Science", email: "adebayo@uni.edu", courses: 3 },
  { id: 2, name: "Dr. Okonkwo", title: "Senior Lecturer", department: "Computer Science", email: "okonkwo@uni.edu", courses: 2 },
  { id: 3, name: "Prof. Ibrahim", title: "Professor", department: "Information Systems", email: "ibrahim@uni.edu", courses: 4 },
];

const students = [
  { id: 1, name: "Ayodele Okonkwo", matric: "CSC/2021/001", level: 400, gpa: 4.2 },
  { id: 2, name: "Chioma Adeyemi", matric: "CSC/2021/002", level: 400, gpa: 4.0 },
];

export default function StaffPage() {
  const [tab, setTab] = useState("staff");
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-slate-600 to-zinc-600 text-white p-6">
        <h1 className="text-2xl font-bold">Staff & Students</h1><p className="text-slate-100">Department management</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4">
          <button onClick={() => setTab("staff")} className={`px-4 py-2 rounded-xl font-medium ${tab === "staff" ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}>Staff</button>
          <button onClick={() => setTab("students")} className={`px-4 py-2 rounded-xl font-medium ${tab === "students" ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}>Students</button>
        </div>
        {tab === "staff" && (
          <div className="space-y-3">
            {staff.map((s) => (
              <div key={s.id} className="bg-white rounded-xl p-4 border border-gray-100 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center text-slate-600 font-bold">{s.name[0]}</div>
                  <div><p className="font-medium text-gray-900">{s.name}</p><p className="text-sm text-gray-500">{s.title} - {s.department}</p></div>
                </div>
                <div className="flex items-center gap-2"><span className="text-sm text-gray-600">{s.courses} courses</span><button className="p-2 text-gray-400 hover:text-gray-600"><Mail className="w-4 h-4" /></button></div>
              </div>
            ))}
          </div>
        )}
        {tab === "students" && (
          <div className="space-y-3">
            {students.map((s) => (
              <div key={s.id} className="bg-white rounded-xl p-4 border border-gray-100 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">{s.name[0]}</div>
                  <div><p className="font-medium text-gray-900">{s.name}</p><p className="text-sm text-gray-500">{s.matric} - Level {s.level}</p></div>
                </div>
                <div className="text-right"><p className="font-bold text-green-600">{s.gpa}</p><p className="text-xs text-gray-500">GPA</p></div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}