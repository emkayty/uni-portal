"use client";
import { useState } from "react";
import { FileText, Download, Share, Upload, Clock, CheckCircle, Search } from "lucide-react";

const documents = [
  { id: 1, name: "Admission Letter", type: "official", uploaded: "2024-01-10", status: "verified" },
  { id: 2, name: "JAMB Result", type: "academic", uploaded: "2024-01-10", status: "verified" },
  { id: 3, name: "O-Level Result", type: "academic", uploaded: "2024-01-12", status: "pending" },
  { id: 4, name: "Birth Certificate", type: "personal", uploaded: "2024-01-12", status: "verified" },
];

export default function DocumentsPage() {
  const [filter, setFilter] = useState("all");
  const filtered = filter === "all" ? documents : documents.filter(d => d.status === filter);
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-slate-600 to-zinc-600 text-white p-6">
        <h1 className="text-2xl font-bold">Documents</h1><p className="text-slate-100">Upload & manage your documents</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4">
          {["all", "verified", "pending"].map((f) => <button key={f} onClick={() => setFilter(f)} className={`px-4 py-2 rounded-xl font-medium capitalize ${filter === f ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}>{f}</button>)}
        </div>
        <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Document</th><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Type</th><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Uploaded</th><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Status</th><th className="px-4 py-3 text-left text-xs font-medium text-gray-500">Actions</th></tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filtered.map((d) => (
                <tr key={d.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3"><div className="flex items-center gap-2"><FileText className="w-4 h-4 text-gray-400" /><span className="font-medium text-gray-900">{d.name}</span></div></td>
                  <td className="px-4 py-3 text-sm text-gray-500 capitalize">{d.type}</td>
                  <td className="px-4 py-3 text-sm text-gray-500">{d.uploaded}</td>
                  <td className="px-4 py-3"><span className={`px-2 py-1 text-xs rounded-full ${d.status === "verified" ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"}`}>{d.status}</span></td>
                  <td className="px-4 py-3"><button className="p-1 text-gray-400 hover:text-gray-600"><Download className="w-4 h-4" /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}