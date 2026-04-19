"use client";
import { useState } from "react";
import { Clock, MapPin, Book, Calendar, ChevronLeft, ChevronRight } from "lucide-react";

const schedule = [
  { day: "Monday", slots: [{ time: "8:00-10:00", course: "CSC401", venue: "Room 101" }, { time: "10:00-12:00", course: "CSC402", venue: "Lab 2" }] },
  { day: "Tuesday", slots: [{ time: "8:00-10:00", course: "CSC403", venue: "Room 201" }] },
  { day: "Wednesday", slots: [{ time: "8:00-10:00", course: "CSC404", venue: "Lab 1" }, { time: "2:00-4:00", course: "CSC405", venue: "Room 105" }] },
  { day: "Thursday", slots: [{ time: "10:00-12:00", course: "CSC401", venue: "Room 101" }] },
  { day: "Friday", slots: [] },
];

export default function TimetablePage() {
  const [week, setWeek] = useState(1);
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white p-6">
        <div className="flex items-center justify-between">
          <div><h1 className="text-2xl font-bold">Class Timetable</h1><p className="text-blue-100">Week {week}</p></div>
          <div className="flex gap-2">
            <button onClick={() => setWeek(Math.max(1, week-1))} className="p-2 bg-white/20 rounded-lg"><ChevronLeft className="w-5 h-5" /></button>
            <button onClick={() => setWeek(week+1)} className="p-2 bg-white/20 rounded-lg"><ChevronRight className="w-5 h-5" /></button>
          </div>
        </div>
      </div>
      <div className="p-4 max-w-7xl mx-auto">
        <div className="space-y-4">
          {schedule.map((day) => (
            <div key={day.day} className="bg-white rounded-xl p-4 border border-gray-100">
              <h3 className="font-semibold text-gray-900 mb-3">{day.day}</h3>
              {day.slots.length === 0 ? <p className="text-gray-500 text-sm">No classes</p> : (
                <div className="space-y-2">
                  {day.slots.map((slot, i) => (
                    <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <Clock className="w-4 h-4 text-gray-400" />
                        <span className="text-sm font-medium text-gray-900">{slot.time}</span>
                      </div>
                      <span className="text-sm text-blue-600 font-medium">{slot.course}</span>
                      <span className="text-sm text-gray-500">{slot.venue}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}