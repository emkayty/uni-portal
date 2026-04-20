"use client";

import { useState } from "react";
import { CreditCard, Download, Share2 } from "lucide-react";

const student = { 
  matric: "CSC/2021/001", 
  name: "Ayodele Okonkwo", 
  department: "Computer Science", 
  level: 400, 
  valid: "2024-12-31", 
  photo: "AO" 
};

export default function IDCardsPage() {
  const [tab, setTab] = useState("idcard");

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
        <h1 className="text-2xl font-bold">Student ID Card</h1>
        <p className="text-blue-100">Digital identification</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4">
          {["idcard", "request", "virtual"].map((t) => (
            <button 
              key={t} 
              onClick={() => setTab(t)} 
              className={`px-4 py-2 rounded-xl font-medium capitalize ${tab === t ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}
            >
              {t}
            </button>
          ))}
        </div>

        {tab === "idcard" && (
          <div className="bg-gradient-to-br from-blue-600 to-indigo-600 rounded-2xl p-6 text-white">
            <div className="flex justify-between items-start mb-6">
              <span className="text-xs">UNIVERSITY ID</span>
              <CreditCard className="w-6 h-6"/>
            </div>
            <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center text-2xl font-bold mb-4">
              {student.photo}
            </div>
            <p className="font-bold text-lg">{student.name}</p>
            <p className="text-blue-100">{student.matric}</p>
            <div className="mt-6 grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-blue-200">Department</p>
                <p>{student.department}</p>
              </div>
              <div>
                <p className="text-blue-200">Level</p>
                <p>Level {student.level}</p>
              </div>
            </div>
            <div className="col-span-2 mt-4">
              <p className="text-blue-200">Valid Until</p>
              <p>{student.valid}</p>
            </div>
            <div className="flex gap-2 mt-6">
              <button className="flex-1 py-2 bg-white text-blue-600 rounded-lg flex items-center justify-center gap-1">
                <Download className="w-4 h-4"/>Download
              </button>
              <button className="flex-1 py-2 border border-white/30 text-white rounded-lg flex items-center justify-center gap-1">
                <Share2 className="w-4 h-4"/>Share
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}