"use client";

import { useState } from "react";
import Link from "next/link";
import { GraduationCap, Book, CreditCard, Calendar, BarChart3, Settings, Bell, Home, FileText, CheckCircle, AlertCircle, ArrowRight, User, LogOut, Menu, X, ChevronDown, Users } from "lucide-react";

interface Student {
  first_name: string;
  student_id: string;
  level: number;
  gpa: number;
}

interface Course {
  code: string;
  title: string;
  units: number;
}

interface NotificationData {
  title: string;
  message: string;
  type: "info" | "warning" | "success";
}

const student: Student = { first_name: "Ayodele", student_id: "CSC/2021/001", level: 400, gpa: 4.2 };

const courses: Course[] = [
  { code: "CSC401", title: "Artificial Intelligence", units: 3 },
  { code: "CSC402", title: "Software Engineering", units: 3 },
  { code: "CSC403", title: "Computer Networks", units: 3 },
  { code: "CSC404", title: "Database Systems", units: 3 },
];

const notifications: NotificationData[] = [
  { title: "Course Registration", message: "Registration opens tomorrow", type: "info" },
  { title: "Exam Timetable", message: "Final exam timetable published", type: "success" },
  { title: "Fee Reminder", message: "Payment deadline in 5 days", type: "warning" },
];

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-14">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <GraduationCap className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-gray-900">UniPortal</span>
          </div>

          <div className="hidden md:flex items-center gap-1">
            <Link href="/" className="px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg">Home</Link>
            <Link href="/courses" className="px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg">Courses</Link>
            <Link href="/grades" className="px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg">Grades</Link>
            <Link href="/finance" className="px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 rounded-lg">Finance</Link>
          </div>

          <div className="flex items-center gap-2">
            <button className="p-2 text-gray-500 relative"><Bell className="w-5 h-5" /><span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span></button>
            <button onClick={() => setUserMenuOpen(!userMenuOpen)} className="flex items-center gap-1 p-1">
              <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center"><span className="text-xs text-white font-medium">AO</span></div>
              <ChevronDown className="w-4 h-4 text-gray-400 hidden sm:block" />
            </button>
            <button onClick={() => setIsOpen(!isOpen)} className="md:hidden p-2 text-gray-500"><Menu className="w-5 h-5" /></button>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden bg-white border-t p-2">
          <Link href="/" className="block px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg">Home</Link>
          <Link href="/courses" className="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg">Courses</Link>
          <Link href="/grades" className="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg">Grades</Link>
          <Link href="/finance" className="block px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg">Finance</Link>
        </div>
      )}
    </nav>
  );
}

function StatCard({ title, value, color }: { title: string; value: string; color: string }) {
  return (
    <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
      <p className="text-xs text-gray-500">{title}</p>
      <p className="text-xl font-bold text-gray-900 mt-1">{value}</p>
    </div>
  );
}

function CourseCard({ course }: { course: Course }) {
  return (
    <div className="bg-white rounded-lg p-3 border border-gray-100">
      <p className="text-xs font-medium text-blue-600">{course.code}</p>
      <p className="text-sm font-medium text-gray-900 mt-1 line-clamp-1">{course.title}</p>
      <p className="text-xs text-gray-500 mt-1">{course.units} units</p>
    </div>
  );
}

function NotificationCard({ notification }: { notification: NotificationData }) {
  const colors: Record<string, string> = { info: "bg-blue-50 text-blue-700", success: "bg-green-50 text-green-700", warning: "bg-amber-50 text-amber-700" };
  return (
    <div className={`p-3 rounded-lg text-sm ${colors[notification.type]}`}>
      <p className="font-medium">{notification.title}</p>
      <p className="text-xs opacity-80 mt-0.5">{notification.message}</p>
    </div>
  );
}

export default function HomePage() {
  const quickLinks = [
    { label: "Courses", href: "/courses", icon: Book },
    { label: "Grades", href: "/grades", icon: FileText },
    { label: "Finance", href: "/finance", icon: CreditCard },
    { label: "Library", href: "/library", icon: Book },
    { label: "Timetable", href: "/timetable", icon: Calendar },
    { label: "Hostel", href: "/hostel", icon: Home },
    { label: "Messages", href: "/messages", icon: Bell },
    { label: "Profile", href: "/profile", icon: User },
    { label: "Registration", href: "/registration", icon: FileText },
    { label: "Attendance", href: "/attendance", icon: CheckCircle },
    { label: "Staff", href: "/staff", icon: Users },
    { label: "Research", href: "/research", icon: BarChart3 },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <Navbar />

      <main className="pt-14">
        <div className="p-4 max-w-7xl mx-auto">
          <div className="mb-4">
            <h1 className="text-xl font-bold text-gray-900">Welcome, {student.first_name}!</h1>
            <p className="text-sm text-gray-500">{student.student_id} • Level {student.level}</p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            <StatCard title="GPA" value={`${student.gpa}/5.0`} color="blue" />
            <StatCard title="Courses" value="5" color="indigo" />
            <StatCard title="Attendance" value="94%" color="green" />
            <StatCard title="Credits" value="118" color="amber" />
          </div>

          <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2 mb-6">
            {quickLinks.map((link) => (
              <Link key={link.label} href={link.href} className="flex flex-col items-center gap-1 p-3 bg-white rounded-xl border border-gray-100 hover:shadow-md transition-all">
                <link.icon className="w-5 h-5 text-blue-600" />
                <span className="text-xs font-medium text-gray-700">{link.label}</span>
              </Link>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white rounded-xl p-4 border border-gray-100">
              <div className="flex items-center justify-between mb-3">
                <h2 className="font-semibold text-gray-900">Current Courses</h2>
                <Link href="/courses" className="text-xs text-blue-600 font-medium">View All</Link>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {courses.map((c) => <CourseCard key={c.code} course={c} />)}
              </div>
            </div>

            <div className="bg-white rounded-xl p-4 border border-gray-100">
              <div className="flex items-center justify-between mb-3">
                <h2 className="font-semibold text-gray-900">Notifications</h2>
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">3 new</span>
              </div>
              <div className="space-y-2">
                {notifications.map((n, i) => <NotificationCard key={i} notification={n} />)}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Mobile Bottom Nav */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 md:hidden">
        <div className="flex justify-around py-2">
          {[{ icon: Home, label: "Home", href: "/" }, { icon: Book, label: "Courses", href: "/courses" }, { icon: CreditCard, label: "Finance", href: "/finance" }, { icon: User, label: "Profile", href: "#" }].map((item) => (
            <Link key={item.label} href={item.href} className="flex flex-col items-center gap-1 px-4 py-1">
              <item.icon className="w-5 h-5 text-gray-600" />
              <span className="text-xs text-gray-600">{item.label}</span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
