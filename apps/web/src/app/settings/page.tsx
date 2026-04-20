"use client";

import { useState } from "react";
import { Bell, Lock, User, Moon, Sun } from "lucide-react";

export default function SettingsPage() {
  const [tab, setTab] = useState("account");
  const [dark, setDark] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-slate-600 to-zinc-600 text-white p-6">
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-slate-100">Customize your experience</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4">
          {["account", "notifications", "privacy", "appearance"].map((t) => (
            <button 
              key={t} 
              onClick={() => setTab(t)} 
              className={`px-4 py-2 rounded-xl font-medium capitalize ${tab === t ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}
            >
              {t}
            </button>
          ))}
        </div>

        {tab === "account" && (
          <div className="bg-white rounded-xl p-4 border border-gray-100 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <User className="w-5 h-5 text-gray-400"/>
                <span>Profile</span>
              </div>
              <button className="text-blue-600">Edit</button>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Lock className="w-5 h-5 text-gray-400"/>
                <span>Password</span>
              </div>
              <button className="text-blue-600">Change</button>
            </div>
          </div>
        )}

        {tab === "notifications" && (
          <div className="bg-white rounded-xl p-4 border border-gray-100 space-y-4">
            <label className="flex items-center justify-between">
              <span>Email notifications</span>
              <input type="checkbox" defaultChecked className="w-5 h-5"/>
            </label>
            <label className="flex items-center justify-between">
              <span>SMS alerts</span>
              <input type="checkbox" defaultChecked className="w-5 h-5"/>
            </label>
            <label className="flex items-center justify-between">
              <span>Push notifications</span>
              <input type="checkbox" className="w-5 h-5"/>
            </label>
          </div>
        )}

        {tab === "appearance" && (
          <div className="bg-white rounded-xl p-4 border border-gray-100">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {dark ? <Moon className="w-5 h-5"/> : <Sun className="w-5 h-5"/>}
                <span>Dark Mode</span>
              </div>
              <button onClick={() => setDark(!dark)} className="px-4 py-2 bg-gray-100 rounded-lg">
                {dark ? "On" : "Off"}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}