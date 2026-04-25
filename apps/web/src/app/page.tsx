"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { 
  GraduationCap, BookOpen, Calendar, CreditCard, Users, MessageSquare,
  Award, FileText, BarChart3, Shield, CheckCircle, ArrowRight, 
  Menu, X, Bell, Search, LogOut, Settings, ChevronRight, Building2,
  Globe, Zap, Lock, Star, TrendingUp, Bookmark, Clipboard, Laptop,
  Wifi, ShieldCheck, Clock, MapPin, Mail, Phone
} from "lucide-react";

const FEATURES = [
  {
    icon: BookOpen,
    title: "Course Registration",
    description: "Register for courses, view prerequisites, and manage your academic load online.",
    color: "bg-blue-600"
  },
  {
    icon: FileText,
    title: "Academic Records",
    description: "Access your transcripts, grades, CGPA, and degree audit reports instantly.",
    color: "bg-green-600"
  },
  {
    icon: CreditCard,
    title: "Fee Payments",
    description: "Pay school fees, hostel, and other charges securely via Remita, Paystack, or bank transfer.",
    color: "bg-amber-600"
  },
  {
    icon: Calendar,
    title: "Academic Calendar",
    description: "Stay updated with exam timetables, lectures, and academic events.",
    color: "bg-purple-600"
  },
  {
    icon: Award,
    title: "Certificates",
    description: "Request and download verified digital certificates and transcripts.",
    color: "bg-indigo-600"
  },
  {
    icon: Users,
    title: "Student Services",
    description: "Hostel applications, SIWES clearance, and departmental clearance.",
    color: "bg-rose-600"
  },
];

const STATS = [
  { value: "50K+", label: "Active Students" },
  { value: "120+", label: "Universities" },
  { value: "99.9%", label: "Uptime" },
  { value: "24/7", label: "Support" },
];

const TESTIMONIALS = [
  {
    name: "Chinedu Emeka",
    role: "Computer Science, UNN",
    text: "UniPortal made course registration so much easier. No more long queues!",
    image: "C"
  },
  {
    name: "Adebola Sarah",
    role: "Economics, UI",
    text: "I can check my grades and pay fees from anywhere. The app is brilliant!",
    image: "A"
  },
  {
    name: "Ibrahim Musa",
    role: "Engineering, FUT Minna",
    text: "The SIWES clearance process was seamless. Highly recommend.",
    image: "I"
  },
];

export default function LandingPage() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState("");

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    
    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString("en-NG", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }) + " WAT");
    }, 1000);
    setCurrentTime(new Date().toLocaleTimeString("en-NG", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }) + " WAT");
    
    return () => { window.removeEventListener("scroll", handleScroll); clearInterval(timer); };
  }, []);

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md shadow-sm' : 'bg-transparent'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
                <GraduationCap className="w-6 h-6 text-white" />
              </div>
              <span className={`font-bold transition ${scrolled ? 'text-slate-900' : 'text-white'}`}>UniPortal</span>
            </Link>

            {/* Desktop Nav */}
            <div className="hidden lg:flex items-center gap-8">
              <a href="#features" className={`text-sm font-medium transition ${scrolled ? 'text-slate-600 hover:text-slate-900' : 'text-white/80 hover:text-white'}`}>Features</a>
              <a href="#universities" className={`text-sm font-medium transition ${scrolled ? 'text-slate-600 hover:text-slate-900' : 'text-white/80 hover:text-white'}`}>Universities</a>
              <a href="#testimonials" className={`text-sm font-medium transition ${scrolled ? 'text-slate-600 hover:text-slate-900' : 'text-white/80 hover:text-white'}`}>Testimonials</a>
              <a href="#contact" className={`text-sm font-medium transition ${scrolled ? 'text-slate-600 hover:text-slate-900' : 'text-white/80 hover:text-white'}`}>Contact</a>
            </div>

            {/* Actions */}
            <div className="hidden lg:flex items-center gap-3">
              <span className={`text-sm ${scrolled ? 'text-slate-500' : 'text-white/60'}`}>{currentTime}</span>
              <Link href="/login" className={`px-4 py-2 rounded-lg text-sm font-medium transition ${scrolled ? 'bg-slate-900 text-white hover:bg-slate-800' : 'bg-white text-slate-900 hover:bg-slate-100'}`}>
                Sign In
              </Link>
            </div>

            {/* Mobile menu button */}
            <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="lg:hidden p-2">
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="lg:hidden bg-white border-t">
            <div className="px-4 py-4 space-y-3">
              <a href="#features" className="block py-2 text-slate-600">Features</a>
              <a href="#universities" className="block py-2 text-slate-600">Universities</a>
              <a href="#testimonials" className="block py-2 text-slate-600">Testimonials</a>
              <a href="#contact" className="block py-2 text-slate-600">Contact</a>
              <Link href="/login" className="block w-full text-center py-3 bg-blue-600 text-white rounded-xl font-medium">
                Sign In
              </Link>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen lg:min-h-[90vh] flex items-center justify-center overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-slate-900">
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500 rounded-full blur-3xl"></div>
            <div className="absolute bottom-20 right-10 w-96 h-96 bg-indigo-500 rounded-full blur-3xl"></div>
            <div className="absolute top-1/3 right-1/4 w-48 h-48 bg-purple-500 rounded-full blur-2xl"></div>
          </div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center pt-20">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 rounded-full backdrop-blur-sm mb-6">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
            <span className="text-sm text-white/80">Serving 50,000+ students across Nigeria</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
            Your Complete
            <br />
            <span className="text-blue-400">University Portal</span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
            The all-in-one academic management platform for Nigerian universities. 
            Register courses, view grades, pay fees, and access services — all in one place.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
            <Link href="/login" className="w-full sm:w-auto px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl flex items-center justify-center gap-2 transition">
              Get Started <ArrowRight className="w-5 h-5" />
            </Link>
            <a href="#features" className="w-full sm:w-auto px-8 py-4 bg-white/10 hover:bg-white/20 text-white font-semibold rounded-xl transition border border-white/20">
              Learn More
            </a>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 max-w-3xl mx-auto">
            {STATS.map((stat, i) => (
              <div key={i} className="text-center">
                <p className="text-3xl font-bold text-white">{stat.value}</p>
                <p className="text-sm text-slate-400">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ChevronRight className="w-6 h-6 text-white/40 rotate-90" />
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 lg:py-32 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-900 mb-4">
              Everything You Need
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              A complete suite of academic tools designed for Nigerian universities
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((feature, i) => (
              <div key={i} className="bg-white rounded-2xl p-6 border border-slate-100 hover:shadow-lg transition card-hover">
                <div className={`w-12 h-12 ${feature.color} rounded-xl flex items-center justify-center mb-4`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{feature.title}</h3>
                <p className="text-slate-600 text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Universities Section */}
      <section id="universities" className="py-20 lg:py-32 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-slate-900 mb-4">
              Trusted by Leading Universities
            </h2>
            <p className="text-lg text-slate-600">
              Join hundreds of institutions already using UniPortal
            </p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-8 lg:gap-16">
            {["UNN", "UI", "UNILAG", "OAU", "UNILORIN", "FUT MINNA"].map((uni, i) => (
              <div key={i} className="text-2xl font-bold text-slate-300">{uni}</div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-20 lg:py-32 bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              What Students Say
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {TESTIMONIALS.map((testimonial, i) => (
              <div key={i} className="bg-slate-800 rounded-2xl p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                    {testimonial.image}
                  </div>
                  <div>
                    <p className="font-semibold text-white">{testimonial.name}</p>
                    <p className="text-sm text-slate-400">{testimonial.role}</p>
                  </div>
                </div>
                <p className="text-slate-300">&quot;{testimonial.text}&quot;</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 lg:py-32 bg-blue-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-lg text-blue-100 mb-8">
            Join thousands of students already using UniPortal
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/login" className="w-full sm:w-auto px-8 py-4 bg-white text-blue-600 font-semibold rounded-xl hover:bg-blue-50 transition">
              Sign In to Portal
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="bg-slate-900 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
                  <GraduationCap className="w-6 h-6 text-white" />
                </div>
                <span className="text-white font-bold">UniPortal</span>
              </div>
              <p className="text-slate-400 text-sm">
                Nigeria's leading university portal solution
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Product</h4>
              <div className="space-y-2 text-sm text-slate-400">
                <a href="#features" className="block">Features</a>
                <a href="#universities" className="block">Universities</a>
                <a href="#" className="block">Pricing</a>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <div className="space-y-2 text-sm text-slate-400">
                <a href="#" className="block">About</a>
                <a href="#" className="block">Contact</a>
                <a href="#" className="block">Careers</a>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-white mb-4">Contact</h4>
              <div className="space-y-2 text-sm text-slate-400">
                <p>support@uniportal.edu</p>
                <p>+234 800 000 0000</p>
                <p>Lagos, Nigeria</p>
              </div>
            </div>
          </div>
          
          <div className="mt-12 pt-8 border-t border-slate-800 text-center text-sm text-slate-500">
            © 2024 UniPortal Nigeria. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}