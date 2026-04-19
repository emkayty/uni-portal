"use client";
import { useState } from "react";
import { FlaskConical, Users, DollarSign, Calendar, FileText, Plus } from "lucide-react";

const projects = [
  { id: 1, title: "AI for Healthcare", department: "Computer Science", budget: 5000000, status: "active", milestones: 3 },
  { id: 2, title: "Blockchain Research", department: "Information Systems", budget: 3000000, status: "active", milestones: 2 },
];

const researchers = [
  { id: 1, name: "Dr. Adebayo", specialization: "Artificial Intelligence", projects: 2 },
  { id: 2, name: "Dr. Okonkwo", specialization: "Machine Learning", projects: 1 },
];

export default function ResearchPage() {
  const [tab, setTab] = useState("projects");
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-violet-600 to-purple-600 text-white p-6">
        <h1 className="text-2xl font-bold">Research & Innovation</h1><p className="text-violet-100">Projects & researchers</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4">
          <button onClick={() => setTab("projects")} className={`px-4 py-2 rounded-xl font-medium ${tab === "projects" ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}>Projects</button>
          <button onClick={() => setTab("researchers")} className={`px-4 py-2 rounded-xl font-medium ${tab === "researchers" ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}>Researchers</button>
        </div>
        {tab === "projects" && (
          <div className="space-y-3">
            {projects.map((p) => (
              <div key={p.id} className="bg-white rounded-xl p-4 border border-gray-100">
                <div className="flex items-start justify-between mb-3">
                  <div><p className="font-medium text-gray-900">{p.title}</p><p className="text-sm text-gray-500">{p.department}</p></div>
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">{p.status}</span>
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <span className="flex items-center gap-1"><DollarSign className="w-4 h-4" />₦{p.budget.toLocaleString()}</span>
                  <span className="flex items-center gap-1"><FileText className="w-4 h-4" />{p.milestones} milestones</span>
                </div>
              </div>
            ))}
          </div>
        )}
        {tab === "researchers" && (
          <div className="space-y-3">
            {researchers.map((r) => (
              <div key={r.id} className="bg-white rounded-xl p-4 border border-gray-100 flex items-center justify-between">
                <div><p className="font-medium text-gray-900">{r.name}</p><p className="text-sm text-gray-500">{r.specialization}</p></div>
                <span className="text-sm text-gray-600">{r.projects} projects</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}