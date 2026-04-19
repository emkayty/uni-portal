"use client";

import { useState } from "react";
import { CreditCard, Receipt, Building, Smartphone, Wallet, AlertCircle, CheckCircle, Download, ChevronRight } from "lucide-react";

const invoices = [
  { id: "INV-2024-001", type: "Tuition", amount: 150000, status: "paid", dueDate: "2024-01-15", paidDate: "2024-01-10" },
  { id: "INV-2024-002", type: "Accommodation", amount: 50000, status: "paid", dueDate: "2024-01-20", paidDate: "2024-01-18" },
  { id: "INV-2024-003", type: "ICT Fee", amount: 10000, status: "pending", dueDate: "2024-02-01", paidDate: null },
  { id: "INV-2024-004", type: "Library Fee", amount: 5000, status: "pending", dueDate: "2024-02-01", paidDate: null },
];

const payments = [
  { id: "PAY-001", method: "Remita", amount: 150000, date: "2024-01-10", status: "success" },
  { id: "PAY-002", method: "Bank Transfer", amount: 50000, date: "2024-01-18", status: "success" },
];

export default function FinancePage() {
  const [activeTab, setActiveTab] = useState("overview");

  const totalPending = invoices.filter(i => i.status === "pending").reduce((sum, i) => sum + i.amount, 0);
  const totalPaid = invoices.filter(i => i.status === "paid").reduce((sum, i) => sum + i.amount, 0);

  const paymentMethods = [
    { name: "Remita", icon: Building, desc: "Federal payment gateway" },
    { name: "Paystack", icon: CreditCard, desc: "Card payments" },
    { name: "Flutterwave", icon: Smartphone, desc: "Mobile money" },
    { name: "Bank Transfer", icon: Wallet, desc: "Direct bank transfer" },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-amber-600 to-orange-600 text-white p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-bold mb-2">Finance & Payments</h1>
          <p className="text-amber-100">Manage your fees and payments</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        {/* Overview Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500 mb-1">Total Paid</p>
            <p className="text-2xl font-bold text-green-600">₦{totalPaid.toLocaleString()}</p>
            <p className="text-xs text-green-600 mt-1">All fees cleared</p>
          </div>
          <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500 mb-1">Pending</p>
            <p className="text-2xl font-bold text-amber-600">₦{totalPending.toLocaleString()}</p>
            <p className="text-xs text-amber-600 mt-1">Due Feb 1, 2024</p>
          </div>
          <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500 mb-1">Scholarship</p>
            <p className="text-2xl font-bold text-blue-600">₦50,000</p>
            <p className="text-xs text-blue-600 mt-1">TETFund Scholarship</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto">
          {["overview", "invoices", "payments", "methods"].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-xl font-medium capitalize transition-colors whitespace-nowrap ${
                activeTab === tab
                  ? "bg-blue-600 text-white"
                  : "bg-white text-gray-600 hover:bg-gray-50 border border-gray-200"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Invoices Tab */}
        {activeTab === "invoices" && (
          <div className="space-y-4">
            {invoices.map((invoice) => (
              <div key={invoice.id} className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="font-semibold text-gray-900">{invoice.type}</p>
                      <span className={`px-2 py-0.5 text-xs font-medium rounded-full ${
                        invoice.status === "paid"
                          ? "bg-green-100 text-green-700"
                          : "bg-amber-100 text-amber-700"
                      }`}>
                        {invoice.status === "paid" ? "Paid" : "Pending"}
                      </span>
                    </div>
                    <p className="text-sm text-gray-500 mt-1">{invoice.id}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xl font-bold text-gray-900">₦{invoice.amount.toLocaleString()}</p>
                    {invoice.status === "paid" ? (
                      <p className="text-xs text-green-600">Paid {invoice.paidDate}</p>
                    ) : (
                      <p className="text-xs text-amber-600">Due {invoice.dueDate}</p>
                    )}
                  </div>
                </div>
                {invoice.status === "pending" && (
                  <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
                    <div className="flex items-center gap-2 text-amber-600">
                      <AlertCircle className="w-4 h-4" />
                      <span className="text-sm">Payment due soon</span>
                    </div>
                    <button className="px-4 py-2 bg-amber-600 text-white text-sm font-medium rounded-lg hover:bg-amber-700">
                      Pay Now
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Payments History Tab */}
        {activeTab === "payments" && (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Reference</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Method</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Date</th>
                  <th className="px-4 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Amount</th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {payments.map((payment) => (
                  <tr key={payment.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-gray-900">{payment.id}</td>
                    <td className="px-4 py-3 text-gray-600">{payment.method}</td>
                    <td className="px-4 py-3 text-gray-600">{payment.date}</td>
                    <td className="px-4 py-3 text-right font-medium text-gray-900">₦{payment.amount.toLocaleString()}</td>
                    <td className="px-4 py-3 text-center">
                      <span className="px-2 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                        {payment.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Payment Methods Tab */}
        {activeTab === "methods" && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {paymentMethods.map((method) => (
              <div key={method.name} className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                    <method.icon className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{method.name}</p>
                    <p className="text-sm text-gray-500">{method.desc}</p>
                  </div>
                </div>
                <button className="w-full mt-4 py-2 border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50 font-medium">
                  Select
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Overview Tab */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            {/* Quick Pay */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-6 text-white">
              <h2 className="text-xl font-bold mb-2">Quick Payment</h2>
              <p className="text-blue-100 mb-4">Pay your pending fees instantly</p>
              <div className="flex flex-col sm:flex-row gap-3">
                <button className="flex-1 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50">
                  Pay All Pending (₦15,000)
                </button>
                <button className="flex-1 py-3 border border-white/30 text-white font-semibold rounded-lg hover:bg-white/10">
                  View Receipts
                </button>
              </div>
            </div>

            {/* Pending Invoices Summary */}
            <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
              <h3 className="font-semibold text-gray-900 mb-4">Pending Invoices</h3>
              <div className="space-y-3">
                {invoices.filter(i => i.status === "pending").map((invoice) => (
                  <div key={invoice.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                    <div>
                      <p className="font-medium text-gray-900">{invoice.type}</p>
                      <p className="text-sm text-gray-500">Due {invoice.dueDate}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-gray-900">₦{invoice.amount.toLocaleString()}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
