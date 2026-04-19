"use client";
import { useState } from "react";
import { User, Mail, Phone, MapPin, Calendar, Book, Award, Camera, Edit } from "lucide-react";

export default function ProfilePage() {
  const [editing, setEditing] = useState(false);
  const student = { first_name: "Ayodele", last_name: "Okonkwo", email: "ayodele@uni.edu", phone: "+2348012345678", level: 400, department: "Computer Science", matric: "CSC/2021/001", gpa: 4.2 };
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-6">
        <div className="flex items-center gap-4">
          <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center text-3xl font-bold">AO</div>
          <div><h1 className="text-2xl font-bold">{student.first_name} {student.last_name}</h1><p className="text-purple-100">{student.matric}</p></div>
        </div>
      </div>
      <div className="p-4 max-w-3xl mx-auto">
        <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm mb-4">
          <div className="flex items-center justify-between mb-4"><h2 className="font-semibold text-gray-900">Personal Information</h2><button onClick={() => setEditing(!editing)} className="text-blue-600 text-sm font-medium">{editing ? "Save" : "Edit"}</button></div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="flex items-center gap-3"><Mail className="w-5 h-5 text-gray-400" /><div><p className="text-xs text-gray-500">Email</p><p className="text-sm font-medium">{student.email}</p></div></div>
            <div className="flex items-center gap-3"><Phone className="w-5 h-5 text-gray-400" /><div><p className="text-xs text-gray-500">Phone</p><p className="text-sm font-medium">{student.phone}</p></div></div>
            <div className="flex items-center gap-3"><Book className="w-5 h-5 text-gray-400" /><div><p className="text-xs text-gray-500">Department</p><p className="text-sm font-medium">{student.department}</p></div></div>
            <div className="flex items-center gap-3"><Award className="w-5 h-5 text-gray-400" /><div><p className="text-xs text-gray-500">Level</p><p className="text-sm font-medium">Level {student.level}</p></div></div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
          <h2 className="font-semibold text-gray-900 mb-4">Academic Summary</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg"><p className="text-xs text-gray-500">GPA</p><p className="text-xl font-bold text-green-600">{student.gpa}</p></div>
            <div className="text-center p-3 bg-gray-50 rounded-lg"><p className="text-xs text-gray-500">Courses</p><p className="text-xl font-bold text-blue-600">5</p></div>
            <div className="text-center p-3 bg-gray-50 rounded-lg"><p className="text-xs text-gray-500">Credits</p><p className="text-xl font-bold text-purple-600">118</p></div>
            <div className="text-center p-3 bg-gray-50 rounded-lg"><p className="text-xs text-gray-500">Standing</p><p className="text-xl font-bold text-gray-900">1st</p></div>
          </div>
        </div>
      </div>
    </div>
  );
}