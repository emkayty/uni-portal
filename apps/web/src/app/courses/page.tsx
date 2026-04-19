"use client";

import { useState } from "react";
import { Book, Clock, CheckCircle, AlertTriangle, Search, Filter, Plus, ChevronRight } from "lucide-react";

const courses = [
  { id: 1, code: "CSC401", title: "Artificial Intelligence", units: 3, lecturer: "Dr. Adebayo", status: "registered", attendance: 95, color: "blue" },
  { id: 2, code: "CSC402", title: "Software Engineering", units: 3, lecturer: "Prof. Okonkwo", status: "registered", attendance: 88, color: "indigo" },
  { id: 3, code: "CSC403", title: "Computer Networks", units: 3, lecturer: "Dr. Ibrahim", status: "registered", attendance: 92, color: "green" },
  { id: 4, code: "CSC404", title: "Database Systems", units: 3, lecturer: "Dr. Chukwu", status: "registered", attendance: 97, color: "amber" },
  { id: 5, code: "CSC405", title: "Project Seminar", units: 2, lecturer: "Prof. Adeyemi", status: "registered", attendance: 100, color: "purple" },
];

const availableCourses = [
  { id: 6, code: "GNS401", title: "Entrepreneurship", units: 2, slots: 50 },
  { id: 7, code: "CSC406", title: "Mobile App Development", units: 3, slots: 30 },
  { id: 8, code: "CSC407", title: "Data Science Fundamentals", units: 3, slots: 40 },
];

export default function CoursesPage() {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const [showRegister, setShowRegister] = useState(false);

  const filteredCourses = courses.filter(c => 
    c.title.toLowerCase().includes(search.toLowerCase()) ||
    c.code.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold mb-2">My Courses</h1>
          <p className="text-blue-100">Semester 2024/2025 - First Semester</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500">Registered</p>
            <p className="text-2xl font-bold text-blue-600">5</p>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500">Total Units</p>
            <p className="text-2xl font-bold text-indigo-600">14</p>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500">Avg Attendance</p>
            <p className="text-2xl font-bold text-green-600">94%</p>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500">Status</p>
            <p className="text-2xl font-bold text-amber-600">Active</p>
          </div>
        </div>

        {/* Search & Actions */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search courses..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Courses</option>
            <option value="registered">Registered</option>
            <option value="completed">Completed</option>
          </select>
          <button
            onClick={() => setShowRegister(true)}
            className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-5 h-5" />
            Add Course
          </button>
        </div>

        {/* Registered Courses */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Registered Courses</h2>
          <div className="grid gap-4">
            {filteredCourses.map((course) => (
              <div key={course.id} className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4">
                    <div className={`w-12 h-12 rounded-xl bg-${course.color}-100 flex items-center justify-center`}>
                      <Book className={`w-6 h-6 text-${course.color}-600`} />
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">{course.title}</p>
                      <p className="text-sm text-gray-500">{course.code} • {course.units} units</p>
                      <p className="text-xs text-gray-400 mt-1">{course.lecturer}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                      Registered
                    </span>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-600">Mon, Wed 8-10am</span>
                    </div>
                    <div className="flex items-center gap-2">
                      {course.attendance >= 90 ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-amber-500" />
                      )}
                      <span className="text-sm text-gray-600">{course.attendance}% Attendance</span>
                    </div>
                  </div>
                  <button className="p-2 text-gray-400 hover:text-gray-600">
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Available Courses */}
        {showRegister && (
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Available Courses</h2>
              <button onClick={() => setShowRegister(false)} className="text-gray-400 hover:text-gray-600">
                ✕
              </button>
            </div>
            <div className="grid gap-3">
              {availableCourses.map((course) => (
                <div key={course.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-xl hover:border-blue-300 transition-colors">
                  <div>
                    <p className="font-medium text-gray-900">{course.title}</p>
                    <p className="text-sm text-gray-500">{course.code} • {course.units} units • {course.slots} slots left</p>
                  </div>
                  <button className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700">
                    Add
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
