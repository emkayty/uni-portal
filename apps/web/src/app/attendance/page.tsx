"use client";
import { useState } from "react";
import { Users, Clock, MapPin, CheckCircle, AlertCircle, Calendar } from "lucide-react";

const attendance = [
  { date: "2024-01-15", course: "CSC401", status: "present", time: "8:00 AM" },
  { date: "2024-01-15", course: "CSC402", status: "present", time: "10:00 AM" },
  { date: "2024-01-14", course: "CSC403", status: "absent", time: "8:00 AM" },
  { date: "2024-01-14", course: "CSC404", status: "present", time: "2:00 PM" },
  { date: "2024-01-13", course: "CSC401", status: "present", time: "8:00 AM" },
];

export default function AttendancePage() {
  const [week, setWeek] = useState(1);
  const stats = { present: 12, absent: 1, total: 13, percentage: 92 };
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-green-600 to-teal-600 text-white p-6">
        <h1 className="text-2xl font-bold">Attendance Record</h1><p className="text-green-100">Week {week}</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-xl p-4 border border-gray-100"><p className="text-sm text-gray-500">Present</p><p className="text-2xl font-bold text-green-600">{stats.present}</p></div>
          <div className="bg-white rounded-xl p-4 border border-gray-100"><p className="text-sm text-gray-500">Absent</p><p className="text-2xl font-bold text-red-600">{stats.absent}</p></div>
          <div className="bg-white rounded-xl p-4 border border-gray-100"><p className="text-sm text-gray-500">Total</p><p className="text-2xl font-bold text-gray-900">{stats.total}</p></div>
          <div className="bg-white rounded-xl p-4 border border-gray-100"><p className="text-sm text-gray-500">Rate</p><p className="text-2xl font-bold text-blue-600">{stats.percentage}%</p></div>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Date</th><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Course</th><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Time</th><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Status</th></tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {attendance.map((a, i) => (
                <tr key={i} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-900">{a.date}</td>
                  <td className="px-4 py-3 text-sm font-medium text-blue-600">{a.course}</td>
                  <td className="px-4 py-3 text-sm text-gray-500">{a.time}</td>
                  <td className="px-4 py-3">{a.status === "present" ? <span className="flex items-center gap-1 text-green-600"><CheckCircle className="w-4 h-4" />Present</span> : <span className="flex items-center gap-1 text-red-600"><AlertCircle className="w-4 h-4" />Absent</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}