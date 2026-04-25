"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { 
  GraduationCap, Book, DollarSign, Clock, Calendar, 
  TrendingUp, Users, FileText, CreditCard, MessageSquare,
  Bell, Search, Menu, X, ChevronRight, Award, LogOut,
  BookOpen, Clipboard, CheckCircle, AlertCircle, Home,
  Settings, User, Mail, Shield, BarChart3, Layers
} from "lucide-react";

// Static data for demo
const DEMO_STUDENT = {
  name: "Abubakar Ibrahim",
  matric: "2021/SCI/001",
  level: "300 Level",
  department: "Computer Science",
  faculty: "Physical Sciences",
  university: "University of Nigeria, Nsukka",
  avatar: null,
  cgpa: "3.85",
  standing: "First Class",
};

const QUICK_ACTIONS = [
  { id: 1, title: "Register Courses", icon: BookOpen, color: "bg-blue-500", link: "/courses" },
  { id: 2, title: "View Results", icon: FileText, color: "bg-green-500", link: "/grades" },
  { id: 3, title: "Pay Fees", icon: DollarSign, color: "bg-amber-500", link: "/finance" },
  { id: 4, title: "Hostel", icon: Home, color: "bg-purple-500", link: "/hostel" },
];

const UPCOMING = [
  { id: 1, title: "Database Systems Exam", date: "Mon, Apr 24", time: "9:00 AM", venue: "LT 3" },
  { id: 2, title: "Software Engineering Project Defense", date: "Wed, Apr 26", time: "2:00 PM", venue: "Lab 2" },
  { id: 3, title: "Industrial Meeting (SIWES)", date: "Fri, Apr 28", time: "10:00 AM", venue: "Hall A" },
];

const RECENT_GRADES = [
  { code: "CSC301", title: "Operating Systems", score: 82, grade: "A" },
  { code: "CSC302", title: "Database Systems", score: 78, grade: "B+" },
  { code: "CSC303", title: "Software Engineering", score: 85, grade: "A" },
  { code: "CSC304", title: "Computer Networks", score: 74, grade: "B" },
];

const ANNOUNCEMENTS = [
  { id: 1, title: "Second Semester Registration Deadline Extended", date: "2 hours ago", urgent: true },
  { id: 2, title: "SIWES Clearance Now Open", date: "1 day ago", urgent: false },
  { id: 3, title: "Hostel Allocation Result Released", date: "2 days ago", urgent: false },
];

export default function DashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState("");
  const [greeting, setGreeting] = useState("");
  
  useEffect(() => {
    const now = new Date();
    setCurrentTime(now.toLocaleDateString("en-NG", { weekday: "long", year: "numeric", month: "long", day: "numeric" }));
    
    const hour = now.getHours();
    if (hour < 12) setGreeting("Good Morning");
    else if (hour < 17) setGreeting("Good Afternoon");
    else setGreeting("Good Evening");
  }, []);

  const navItems = [
    { icon: Home, label: "Dashboard", href: "/dashboard", active: true },
    { icon: BookOpen, label: "Courses", href: "/courses" },
    { icon: FileText, label: "Results", href: "/grades" },
    { icon: DollarSign, label: "Finance", href: "/finance" },
    { icon: CreditCard, label: "Payments", href: "/payments" },
    { icon: Calendar, label: "Timetable", href: "/timetable" },
    { icon: Users, label: "Attendance", href: "/attendance" },
    { icon: Book, label: "Library", href: "/library" },
    { icon: MessageSquare, label: "Messages", href: "/messages", badge: 3 },
    { icon: Award, label: "Certificates", href: "/certificates" },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-72 bg-slate-900 transform transition-transform duration-300 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0`}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6 border-b border-slate-800">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
                <GraduationCap className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-white font-bold">UniPortal</h1>
                <p className="text-slate-400 text-xs">Student Portal</p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 overflow-y-auto">
            <div className="space-y-1">
              {navItems.map((item) => (
                <Link 
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition ${
                    item.active 
                      ? 'bg-blue-600 text-white' 
                      : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="flex-1">{item.label}</span>
                  {item.badge && (
                    <span className="bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                      {item.badge}
                    </span>
                  )}
                </Link>
              ))}
            </div>
          </nav>

          {/* Bottom section */}
          <div className="p-4 border-t border-slate-800">
            <Link href="/settings" className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-xl transition">
              <Settings className="w-5 h-5" />
              <span>Settings</span>
            </Link>
            <Link href="/login" className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-xl transition">
              <LogOut className="w-5 h-5" />
              <span>Sign Out</span>
            </Link>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Header */}
        <header className="bg-white border-b border-slate-200 px-4 lg:px-6 py-4 sticky top-0 z-40">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 hover:bg-slate-100 rounded-xl">
                <Menu className="w-6 h-6" />
              </button>
              <div>
                <h1 className="text-xl font-bold text-slate-900">{greeting}, {DEMO_STUDENT.name.split(' ')[0]}! 👋</h1>
                <p className="text-slate-500 text-sm">{currentTime}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Search */}
              <div className="hidden md:flex items-center gap-2 bg-slate-100 px-4 py-2.5 rounded-xl">
                <Search className="w-4 h-4 text-slate-400" />
                <input 
                  type="text" 
                  placeholder="Search..." 
                  className="bg-transparent outline-none text-sm w-40"
                />
              </div>

              {/* Notifications */}
              <button className="relative p-2.5 bg-slate-100 rounded-xl hover:bg-slate-200 transition">
                <Bell className="w-5 h-5 text-slate-600" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>

              {/* Profile */}
              <div className="flex items-center gap-3 pl-3 border-l border-slate-200">
                <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                  {DEMO_STUDENT.name.charAt(0)}
                </div>
                <div className="hidden lg:block">
                  <p className="text-sm font-medium text-slate-900">{DEMO_STUDENT.matric}</p>
                  <p className="text-xs text-slate-500">{DEMO_STUDENT.level}</p>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 p-4 lg:p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            {/* Quick stats */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white rounded-2xl p-5 border border-slate-100 card-hover">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-blue-600" />
                  </div>
                  <span className="text-green-600 text-sm font-medium">+0.15</span>
                </div>
                <p className="text-2xl font-bold text-slate-900">{DEMO_STUDENT.cgpa}</p>
                <p className="text-slate-500 text-sm">Current CGPA</p>
              </div>

              <div className="bg-white rounded-2xl p-5 border border-slate-100 card-hover">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
                    <Award className="w-5 h-5 text-green-600" />
                  </div>
                </div>
                <p className="text-2xl font-bold text-slate-900">{DEMO_STUDENT.standing}</p>
                <p className="text-slate-500 text-sm">Class Standing</p>
              </div>

              <div className="bg-white rounded-2xl p-5 border border-slate-100 card-hover">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center">
                    <CreditCard className="w-5 h-5 text-amber-600" />
                  </div>
                  <span className="text-green-600 text-sm font-medium">Paid</span>
                </div>
                <p className="text-2xl font-bold text-slate-900">₦45,000</p>
                <p className="text-slate-500 text-sm">School Fees</p>
              </div>

              <div className="bg-white rounded-2xl p-5 border border-slate-100 card-hover">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
                    <Layers className="w-5 h-5 text-purple-600" />
                  </div>
                </div>
                <p className="text-2xl font-bold text-slate-900">5</p>
                <p className="text-slate-500 text-sm">Courses Registered</p>
              </div>
            </div>

            {/* Quick actions */}
            <div className="bg-white rounded-2xl p-5 border border-slate-100">
              <h2 className="text-lg font-bold text-slate-900 mb-4">Quick Actions</h2>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                {QUICK_ACTIONS.map((action) => (
                  <Link 
                    key={action.id}
                    href={action.link}
                    className="flex flex-col items-center gap-3 p-5 rounded-xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50 transition card-hover"
                  >
                    <div className={`w-12 h-12 ${action.color} rounded-xl flex items-center justify-center`}>
                      <action.icon className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-sm font-medium text-slate-700 text-center">{action.title}</span>
                  </Link>
                ))}
              </div>
            </div>

            <div className="grid lg:grid-cols-3 gap-6">
              {/* Upcoming events */}
              <div className="lg:col-span-2 bg-white rounded-2xl p-5 border border-slate-100">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-bold text-slate-900">Upcoming</h2>
                  <Link href="/calendar" className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1">
                    View all <ChevronRight className="w-4 h-4" />
                  </Link>
                </div>
                <div className="space-y-3">
                  {UPCOMING.map((event) => (
                    <div key={event.id} className="flex items-center gap-4 p-4 bg-slate-50 rounded-xl">
                      <div className="w-12 h-12 bg-blue-100 rounded-xl flex flex-col items-center justify-center">
                        <span className="text-xs text-blue-600 uppercase">{event.date.split(' ')[0]}</span>
                        <span className="text-lg font-bold text-blue-600">{event.date.split(' ')[1]}</span>
                      </div>
                      <div className="flex-1">
                        <p className="font-medium text-slate-900">{event.title}</p>
                        <p className="text-sm text-slate-500">{event.time} • {event.venue}</p>
                      </div>
                      <ChevronRight className="w-5 h-5 text-slate-400" />
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent grades */}
              <div className="bg-white rounded-2xl p-5 border border-slate-100">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-bold text-slate-900">Recent Grades</h2>
                  <Link href="/grades" className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1">
                    View all <ChevronRight className="w-4 h-4" />
                  </Link>
                </div>
                <div className="space-y-3">
                  {RECENT_GRADES.map((grade) => (
                    <div key={grade.code} className="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                      <div>
                        <p className="font-medium text-slate-900">{grade.code}</p>
                        <p className="text-xs text-slate-500">{grade.title}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold text-slate-900">{grade.grade}</p>
                        <p className="text-xs text-slate-500">{grade.score}%</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Announcements */}
            <div className="bg-white rounded-2xl p-5 border border-slate-100">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-slate-900">Announcements</h2>
                <Link href="/messages" className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1">
                  View all <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
              <div className="space-y-3">
                {ANNOUNCEMENTS.map((ann) => (
                  <div key={ann.id} className="flex items-start gap-4 p-4 bg-slate-50 rounded-xl">
                    {ann.urgent ? (
                      <AlertCircle className="w-5 h-5 text-red-500 mt-0.5" />
                    ) : (
                      <Bell className="w-5 h-5 text-slate-400 mt-0.5" />
                    )}
                    <div className="flex-1">
                      <p className={`font-medium ${ann.urgent ? 'text-red-600' : 'text-slate-900'}`}>{ann.title}</p>
                      <p className="text-sm text-slate-500">{ann.date}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}