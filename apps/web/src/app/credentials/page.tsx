"use client";

import { useState } from "react";
import { QrCode, Share2, CheckCircle } from "lucide-react";

const credentials = [
  { id: "cred-001", type: "Certificate", title: "Bachelor of Science", issue: "2024-01-15", status: "active", verified: true },
  { id: "cred-002", type: "Badge", title: "First Class Honours", issue: "2024-01-15", status: "active", verified: true },
  { id: "cred-003", type: "Credential", title: "Digital Skills", issue: "2024-01-10", status: "active", verified: true }
];

export default function CredentialsPage() {
  const [tab, setTab] = useState("credentials");

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6">
        <h1 className="text-2xl font-bold">Credentials</h1>
        <p className="text-indigo-100">Blockchain-verified credentials</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4">
          {["credentials", "verify", "badge"].map((t) => (
            <button 
              key={t} 
              onClick={() => setTab(t)} 
              className={`px-4 py-2 rounded-xl font-medium capitalize ${tab === t ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}
            >
              {t}
            </button>
          ))}
        </div>

        {tab === "credentials" && (
          <div className="space-y-3">
            {credentials.map((c) => (
              <div key={c.id} className="bg-white rounded-xl p-4 border border-gray-100">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold text-gray-900">{c.title}</p>
                    <p className="text-sm text-gray-500">{c.type} - {c.issue}</p>
                  </div>
                  {c.verified && <CheckCircle className="w-5 h-5 text-green-500"/>}
                </div>
                <div className="flex gap-2 mt-3">
                  <button className="flex-1 py-2 bg-gray-100 text-gray-700 text-sm rounded-lg flex items-center justify-center gap-1">
                    <QrCode className="w-4 h-4"/>View
                  </button>
                  <button className="flex-1 py-2 bg-indigo-600 text-white text-sm rounded-lg flex items-center justify-center gap-1">
                    <Share2 className="w-4 h-4"/>Share
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {tab === "verify" && (
          <div className="bg-white rounded-xl p-6 border border-gray-100 text-center">
            <QrCode className="w-20 h-20 mx-auto text-indigo-600 mb-3"/>
            <p className="text-gray-500">Scan QR code to verify</p>
          </div>
        )}
      </div>
    </div>
  );
}