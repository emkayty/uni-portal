"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { GraduationCap, Eye, EyeOff, Loader2, AlertCircle, Building2, Mail, Lock, ArrowRight, Shield } from "lucide-react";
import Link from "next/link";

// Nigerian universities for selection
const NIGERIAN_UNIVERSITIES = [
  { id: "unn", name: "University of Nigeria, Nsukka", short: "UNN", location: "Nsukka, Enugu" },
  { id: "ui", name: "University of Ibadan", short: "UI", location: "Ibadan, Oyo" },
  { id: "uniLag", name: "University of Lagos", short: "UNILAG", location: "Lagos, Lagos" },
  { id: "obuda", name: "Obafemi Awolowo University", short: "OAU", location: "Ile-Ife, Osun" },
  { id: "unilorin", name: "University of Ilorin", short: "UNILORIN", location: "Ilorin, Kwara" },
  { id: "fsbs", name: "Federal University of Technology", short: "FUT", location: "Minna, Niger" },
];

export default function LoginPage() {
  const router = useRouter();
  const [selectedUni, setSelectedUni] = useState("");
  const [matricNumber, setMatricNumber] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [currentTime, setCurrentTime] = useState("");
  
  // Real-time greeting based on time
  useEffect(() => {
    const now = new Date();
    setCurrentTime(now.toLocaleTimeString("en-NG", { hour: "2-digit", minute: "2-digit" }));
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString("en-NG", { hour: "2-digit", minute: "2-digit" }));
    }, 60000);
    return () => clearInterval(timer);
  }, []);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good Morning";
    if (hour < 17) return "Good Afternoon";
    return "Good Evening";
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Simulate API call
    setTimeout(() => {
      if (matricNumber && password) {
        // Check if it's a demo login
        if (matricNumber.toLowerCase() === "demo" || password === "demo") {
          router.push("/dashboard");
        } else {
          setError("Invalid credentials. Try 'demo' for both fields.");
        }
      } else {
        setError("Please enter your matric number and password");
      }
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
        {/* Abstract pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-72 h-72 bg-blue-500 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-indigo-500 rounded-full blur-3xl"></div>
          <div className="absolute top-1/2 left-1/2 w-48 h-48 bg-purple-500 rounded-full blur-2xl"></div>
        </div>
        
        <div className="relative z-10 flex flex-col justify-center items-center w-full p-12 text-center">
          <div className="w-24 h-24 bg-white/10 rounded-3xl flex items-center justify-center mb-8 backdrop-blur-sm border border-white/20">
            <GraduationCap className="w-12 h-12 text-white" />
          </div>
          
          <h1 className="text-5xl font-bold text-white mb-4 tracking-tight">
            UniPortal
          </h1>
          <p className="text-xl text-slate-300 mb-2">Nigerian University Portal</p>
          <p className="text-slate-400 max-w-md">
            Your all-in-one academic management platform for results, registration, fees, and more.
          </p>

          {/* Features */}
          <div className="mt-12 grid grid-cols-2 gap-4 text-left">
            <div className="flex items-center gap-3 text-slate-300">
              <div className="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                <Building2 className="w-4 h-4 text-blue-400" />
              </div>
              <span className="text-sm">10+ Universities</span>
            </div>
            <div className="flex items-center gap-3 text-slate-300">
              <div className="w-8 h-8 bg-green-500/20 rounded-lg flex items-center justify-center">
                <Shield className="w-4 h-4 text-green-400" />
              </div>
              <span className="text-sm">Secure & Verified</span>
            </div>
          </div>

          {/* Time display */}
          <div className="mt-12 text-slate-500">
            <span className="text-sm">{currentTime} WAT</span>
          </div>
        </div>
      </div>

      {/* Right Panel - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12 bg-white">
        <div className="w-full max-w-md">
          {/* Mobile header */}
          <div className="lg:hidden mb-8 text-center">
            <div className="w-14 h-14 bg-slate-900 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <GraduationCap className="w-7 h-7 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-slate-900">UniPortal</h1>
            <p className="text-slate-500 text-sm">Nigerian University Portal</p>
          </div>

          <div className="mb-8">
            <h2 className="text-3xl font-bold text-slate-900">{getGreeting()}</h2>
            <p className="text-slate-500 mt-1">Sign in to continue to your dashboard</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-100 rounded-xl flex items-start gap-3 text-red-600">
              <AlertCircle className="w-5 h-5 mt-0.5 flex-shrink-0" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-5">
            {/* University Selection */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">
                Select University
              </label>
              <select
                value={selectedUni}
                onChange={(e) => setSelectedUni(e.target.value)}
                className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition bg-white"
              >
                <option value="">Choose your university</option>
                {NIGERIAN_UNIVERSITIES.map((uni) => (
                  <option key={uni.id} value={uni.id}>
                    {uni.name} ({uni.short})
                  </option>
                ))}
              </select>
            </div>

            {/* Matric Number */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">
                Matriculation Number
              </label>
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                  <Mail className="w-5 h-5" />
                </div>
                <input
                  type="text"
                  value={matricNumber}
                  onChange={(e) => setMatricNumber(e.target.value.toUpperCase())}
                  placeholder="e.g., 20/SC/1234"
                  className="w-full pl-12 pr-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition uppercase placeholder:text-slate-300"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-sm font-medium text-slate-700">
                  Password
                </label>
                <Link href="/forgot-password" className="text-sm text-blue-600 hover:text-blue-700">
                  Forgot password?
                </Link>
              </div>
              <div className="relative">
                <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                  <Lock className="w-5 h-5" />
                </div>
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full pl-12 pr-12 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Remember me */}
            <div className="flex items-center">
              <input
                type="checkbox"
                id="remember"
                className="w-4 h-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500"
              />
              <label htmlFor="remember" className="ml-2 text-sm text-slate-600">
                Remember me for 30 days
              </label>
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded-xl flex items-center justify-center gap-2 transition disabled:opacity-70 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Signing in...</span>
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>

            {/* Demo hint */}
            <p className="text-center text-sm text-slate-500">
              Demo mode: Enter <span className="font-mono bg-slate-100 px-1.5 py-0.5 rounded">demo</span> for both fields
            </p>
          </form>

          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-slate-100 text-center">
            <p className="text-sm text-slate-500">
              Need help?{" "}
              <a href="#" className="text-blue-600 hover:text-blue-700 font-medium">
                Contact Support
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}