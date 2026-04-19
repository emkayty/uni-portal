"use client";
import { useState } from "react";
import { Book, Search, Calendar, Download, Clock, MapPin, CheckCircle, AlertCircle } from "lucide-react";

const books = [
  { id: 1, title: "Introduction to Algorithms", author: "Cormen", status: "available", due: null },
  { id: 2, title: "Database System Concepts", author: "Silberschatz", status: "borrowed", due: "2024-02-15" },
  { id: 3, title: "Artificial Intelligence", author: "Russell & Norvig", status: "available", due: null },
  { id: 4, title: "Computer Networks", author: "Tanenbaum", status: "available", due: null },
];

export default function LibraryPage() {
  const [search, setSearch] = useState("");
  const [activeTab, setActiveTab] = useState("search");

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6">
        <h1 className="text-2xl font-bold">Library Services</h1>
        <p className="text-indigo-100">Digital resources & borrowing</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="flex gap-2 mb-4 overflow-x-auto">
          {["search", "borrowed", "digital", "rooms"].map((tab) => (
            <button key={tab} onClick={() => setActiveTab(tab)} className={`px-4 py-2 rounded-xl font-medium capitalize ${activeTab === tab ? "bg-blue-600 text-white" : "bg-white text-gray-600"}`}>
              {tab}
            </button>
          ))}
        </div>
        <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input type="text" placeholder="Search library catalogue..." value={search} onChange={(e) => setSearch(e.target.value)} className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl" />
          </div>
          <div className="space-y-3">
            {books.map((book) => (
              <div key={book.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
                <div>
                  <p className="font-medium text-gray-900">{book.title}</p>
                  <p className="text-sm text-gray-500">{book.author}</p>
                </div>
                <div className="flex items-center gap-2">
                  {book.status === "available" ? <CheckCircle className="w-5 h-5 text-green-500" /> : <AlertCircle className="w-5 h-5 text-amber-500" />}
                  <span className={`text-sm ${book.status === "available" ? "text-green-600" : "text-amber-600"}`}>{book.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}