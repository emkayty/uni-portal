"use client";
import { useState } from "react";
import { BookOpen, CheckCircle, AlertCircle, Clock, Plus, Search, Filter } from "lucide-react";

const courses = [
  { id: 1, code: "CSC401", title: "Artificial Intelligence", units: 3, status: "open", seats: 45 },
  { id: 2, code: "CSC402", title: "Software Engineering", units: 3, status: "open", seats: 30 },
  { id: 3, code: "CSC403", title: "Computer Networks", units: 3, status: "closed", seats: 0 },
  { id: 4, code: "GNS401", title: "Entrepreneurship", units: 2, status: "open", seats: 100 },
];

const registered = [
  { code: "CSC401", title: "Artificial Intelligence", units: 3 },
  { code: "CSC402", title: "Software Engineering", units: 3 },
  { code: "CSC404", title: "Database Systems", units: 3 },
];

export default function RegistrationPage() {
  const [step, setStep] = useState(1);
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
        <h1 className="text-2xl font-bold">Course Registration</h1><p className="text-blue-100">Semester 2024/2025 - First Semester</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4">
          {[1, 2, 3].map((s) => <button key={s} onClick={() => setStep(s)} className={`flex-1 py-2 rounded-lg font-medium ${step === s ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}>Step {s}</button>)}
        </div>
        {step === 1 && (
          <div className="bg-white rounded-xl p-4 border border-gray-100">
            <h2 className="font-semibold text-gray-900 mb-4">Registered Courses ({registered.length})</h2>
            <div className="space-y-2 mb-4">
              {registered.map((c) => (
                <div key={c.code} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                  <div><p className="font-medium text-gray-900">{c.code}</p><p className="text-sm text-gray-500">{c.title}</p></div>
                  <div className="flex items-center gap-2"><span className="text-sm text-gray-600">{c.units} units</span><CheckCircle className="w-5 h-5 text-green-500" /></div>
                </div>
              ))}
            </div>
            <div className="text-lg font-semibold text-gray-900">Total Units: <span className="text-blue-600">9</span></div>
          </div>
        )}
        {step === 2 && (
          <div className="bg-white rounded-xl p-4 border border-gray-100">
            <h2 className="font-semibold text-gray-900 mb-4">Available Courses</h2>
            <div className="space-y-2">
              {courses.map((c) => (
                <div key={c.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                  <div><p className="font-medium text-gray-900">{c.code}</p><p className="text-sm text-gray-500">{c.title}</p></div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">{c.units} units</span>
                    {c.status === "open" ? <button className="px-3 py-1 bg-green-600 text-white text-sm rounded-lg">Add</button> : <span className="text-red-500 text-sm">Closed</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        {step === 3 && (
          <div className="bg-white rounded-xl p-4 border border-gray-100 text-center"><h2 className="font-semibold text-gray-900 mb-4">Review & Submit</h2><p className="text-gray-500">Confirm your course selection</p><button className="mt-4 px-6 py-2 bg-green-600 text-white font-medium rounded-lg">Submit Registration</button></div>
        )}
      </div>
    </div>
  );
}