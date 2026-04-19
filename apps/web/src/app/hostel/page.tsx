"use client";
import { useState } from "react";
import { Home, Bed, Users, Calendar, MapPin, CheckCircle, X } from "lucide-react";

const rooms = [
  { id: 1, block: "A", room: "101", beds: 4, occupied: 2, type: "4-bed", status: "available" },
  { id: 2, block: "A", room: "102", beds: 4, occupied: 4, type: "4-bed", status: "full" },
  { id: 3, block: "B", room: "201", beds: 2, occupied: 1, type: "2-bed", status: "available" },
];

export default function HostelPage() {
  const [selectedRoom, setSelectedRoom] = useState<number | null>(null);
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-amber-600 to-orange-600 text-white p-6">
        <h1 className="text-2xl font-bold">Hostel & Accommodation</h1>
        <p className="text-amber-100">Apply for on-campus housing</p>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-xl p-4 border border-gray-100"><p className="text-sm text-gray-500">Available Rooms</p><p className="text-2xl font-bold text-green-600">24</p></div>
          <div className="bg-white rounded-xl p-4 border border-gray-100"><p className="text-sm text-gray-500">Your Application</p><p className="text-2xl font-bold text-blue-600">Pending</p></div>
          <div className="bg-white rounded-xl p-4 border border-gray-100"><p className="text-sm text-gray-500">Check-in Date</p><p className="text-2xl font-bold text-gray-900">Aug 15</p></div>
        </div>
        <div className="bg-white rounded-xl p-4 border border-gray-100">
          <h2 className="font-semibold text-gray-900 mb-4">Available Rooms</h2>
          <div className="space-y-3">
            {rooms.map((room) => (
              <div key={room.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-xl">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center"><Bed className="w-5 h-5 text-amber-600" /></div>
                  <div><p className="font-medium text-gray-900">{room.block} - {room.room}</p><p className="text-sm text-gray-500">{room.type}</p></div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-600">{room.occupied}/{room.beds} occupied</span>
                  <button onClick={() => setSelectedRoom(room.id)} disabled={room.status === "full"} className="px-3 py-1 bg-blue-600 text-white text-sm rounded-lg disabled:opacity-50">Apply</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}