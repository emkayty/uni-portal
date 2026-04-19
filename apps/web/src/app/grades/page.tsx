"use client";

import { useState } from "react";
import { Award, TrendingUp, TrendingDown, Minus, Download, BarChart3, Calendar } from "lucide-react";

const semesters = [
  { id: 1, name: "2024/2025 - First", gpa: 4.2, status: "current" },
  { id: 2, name: "2023/2024 - Second", gpa: 4.0, status: "completed" },
  { id: 3, name: "2023/2024 - First", gpa: 3.8, status: "completed" },
  { id: 4, name: "2022/2023 - Second", gpa: 3.9, status: "completed" },
];

const grades = [
  { code: "CSC401", title: "Artificial Intelligence", units: 3, score: 85, grade: "A", points: 5.0 },
  { code: "CSC402", title: "Software Engineering", units: 3, score: 78, grade: "B+", points: 4.5 },
  { code: "CSC403", title: "Computer Networks", units: 3, score: 92, grade: "A", points: 5.0 },
  { code: "CSC404", title: "Database Systems", units: 3, score: 88, grade: "A", points: 5.0 },
  { code: "CSC405", title: "Project Seminar", units: 2, score: 90, grade: "A", points: 5.0 },
];

export default function GradesPage() {
  const [selectedSemester, setSelectedSemester] = useState(1);

  const getGradeColor = (grade: string) => {
    if (grade.startsWith("A")) return "bg-green-100 text-green-700";
    if (grade.startsWith("B")) return "bg-blue-100 text-blue-700";
    if (grade.startsWith("C")) return "bg-amber-100 text-amber-700";
    return "bg-gray-100 text-gray-700";
  };

  const currentSemester = semesters.find(s => s.id === selectedSemester);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold mb-2">My Grades & Results</h1>
          <p className="text-green-100">Track your academic performance</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        {/* GPA Overview */}
        <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm mb-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <p className="text-sm text-gray-500 mb-1">Current GPA</p>
              <p className="text-4xl font-bold text-gray-900">{currentSemester?.gpa}.0 <span className="text-lg text-gray-400 font-normal">/ 5.0</span></p>
            </div>
            <div className="flex gap-6">
              <div className="text-center">
                <p className="text-sm text-gray-500">Total Units</p>
                <p className="text-xl font-semibold text-gray-900">118</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-500">CGPA</p>
                <p className="text-xl font-semibold text-gray-900">4.0</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-500">Class</p>
                <p className="text-xl font-semibold text-gray-900">First Class</p>
              </div>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
              <Download className="w-4 h-4" />
              Download Transcript
            </button>
          </div>
        </div>

        {/* Semester Tabs */}
        <div className="flex gap-2 overflow-x-auto pb-4 mb-6">
          {semesters.map((sem) => (
            <button
              key={sem.id}
              onClick={() => setSelectedSemester(sem.id)}
              className={`flex-shrink-0 px-4 py-2 rounded-xl font-medium transition-colors ${
                selectedSemester === sem.id
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-600 hover:bg-gray-50 border border-gray-200"
              }`}
            >
              {sem.name}
            </button>
          ))}
        </div>

        {/* Grades Table */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <div className="p-4 border-b border-gray-100">
            <h2 className="font-semibold text-gray-900">{currentSemester?.name} Results</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Code</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Course Title</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Units</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Score</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Grade</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Points</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {grades.map((grade, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-blue-600">{grade.code}</td>
                    <td className="px-4 py-3 text-gray-900">{grade.title}</td>
                    <td className="px-4 py-3 text-center text-gray-600">{grade.units}</td>
                    <td className="px-4 py-3 text-center font-medium text-gray-900">{grade.score}</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getGradeColor(grade.grade)}`}>
                        {grade.grade}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center text-gray-600">{grade.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Performance Chart Placeholder */}
        <div className="mt-6 bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
          <h2 className="font-semibold text-gray-900 mb-4">GPA Trend</h2>
          <div className="h-48 flex items-end justify-around gap-2">
            {[4.2, 4.0, 3.8, 3.9, 4.1, 4.0].map((gpa, i) => (
              <div key={i} className="flex flex-col items-center gap-2">
                <div
                  className="w-8 sm:w-12 bg-gradient-to-t from-blue-600 to-blue-400 rounded-t-lg"
                  style={{ height: `${gpa * 20}%` }}
                ></div>
                <span className="text-xs text-gray-500">Y{i + 1}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
