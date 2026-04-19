"use client";
import { useState } from "react";
import { MessageSquare, Send, Bell, Mail, Check, CheckCheck } from "lucide-react";

const conversations = [
  { id: 1, from: "Registrar", subject: "Course Registration", preview: "Your registration is been processed...", time: "2:30 PM", unread: true },
  { id: 2, from: "Finance Office", subject: "Fee Payment", preview: "Please clear your outstanding fees...", time: "Yesterday", unread: false },
  { id: 3, from: "Department", subject: "Exam Timetable", preview: "The exam timetable has been...", time: "Yesterday", unread: false },
];

export default function MessagesPage() {
  const [activeConv, setActiveConv] = useState<number | null>(1);
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-6">
        <h1 className="text-2xl font-bold">Messages</h1><p className="text-green-100">Announcements & notifications</p>
      </div>
      <div className="flex h-[calc(100vh-180px)]">
        <div className="w-full md:w-1/3 border-r border-gray-200 bg-white overflow-y-auto">
          {conversations.map((conv) => (
            <div key={conv.id} onClick={() => setActiveConv(conv.id)} className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 ${activeConv === conv.id ? "bg-blue-50 border-l-4 border-l-blue-600" : ""}`}>
              <div className="flex items-start justify-between"><p className="font-medium text-gray-900">{conv.from}</p>{conv.unread && <span className="w-2 h-2 bg-blue-600 rounded-full"></span>}</div>
              <p className="text-sm text-gray-600">{conv.subject}</p>
              <p className="text-xs text-gray-400 truncate">{conv.preview}</p>
              <p className="text-xs text-gray-400 mt-1">{conv.time}</p>
            </div>
          ))}
        </div>
        <div className="hidden md:flex flex-1 flex-col">
          {activeConv ? (
            <div className="flex-1 p-4"><p className="text-gray-500">Select a conversation</p></div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-gray-500">Select a message to view</div>
          )}
        </div>
      </div>
    </div>
  );
}