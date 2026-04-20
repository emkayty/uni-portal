"use client";

import { useState } from "react";
import { TrendingUp } from "lucide-react";

const stats = { gpa: 4.2, rank: 5, percentile: 98, trend: "up" };

export default function AnalyticsPage() {
  const [tab, setTab] = useState("overview");

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white p-6">
        <h1 className="text-2xl font-bold">Analytics</h1>
        <p className="text-blue-100">Academic insights and predictions</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4">
          {["overview", "predictions", "trends"].map((t) => (
            <button 
              key={t} 
              onClick={() => setTab(t)} 
              className={`px-4 py-2 rounded-xl font-medium capitalize ${tab === t ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}
            >
              {t}
            </button>
          ))}
        </div>
        
        {tab === "overview" && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-xl p-4 border border-gray-100">
              <p className="text-sm text-gray-500">GPA</p>
              <p className="text-2xl font-bold text-green-600">{stats.gpa}</p>
            </div>
            <div className="bg-white rounded-xl p-4 border border-gray-100">
              <p className="text-sm text-gray-500">Rank</p>
              <p className="text-2xl font-bold text-blue-600">#{stats.rank}</p>
            </div>
            <div className="bg-white rounded-xl p-4 border border-gray-100">
              <p className="text-sm text-gray-500">Percentile</p>
              <p className="text-2xl font-bold text-purple-600">{stats.percentile}%</p>
            </div>
            <div className="bg-white rounded-xl p-4 border border-gray-100">
              <p className="text-sm text-gray-500">Trend</p>
              <p className="text-2xl font-bold text-green-600 flex items-center gap-1">
                <TrendingUp className="w-5 h-5"/>Up
              </p>
            </div>
          </div>
        )}

        {tab === "predictions" && (
          <div className="bg-white rounded-xl p-4 border border-gray-100">
            <h2 className="font-semibold text-gray-900 mb-3">AI Predictions</h2>
            <div className="space-y-3">
              <div className="p-3 bg-green-50 rounded-lg">
                <p className="font-medium text-gray-900">First Class Probability</p>
                <p className="text-sm text-green-600">92% - Excellent standing</p>
              </div>
              <div className="p-3 bg-blue-50 rounded-lg">
                <p className="font-medium text-gray-900">Course Performance</p>
                <p className="text-sm text-blue-600">AI predicts A in all courses</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}