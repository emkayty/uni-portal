"use client";

import { useState } from "react";
import { View, Text, ScrollView, TouchableOpacity, SafeAreaView, StyleSheet } from "react-native";

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
  id: string;
  title: string;
  message: string;
  type: "info" | "warning" | "success";
}

const student: Student = {
  first_name: "Ayodele",
  student_id: "CSC/2021/001",
  level: 400,
  gpa: 4.2,
};

const courses: Course[] = [
  { code: "CSC401", title: "Artificial Intelligence", units: 3 },
  { code: "CSC402", title: "Software Engineering", units: 3 },
  { code: "CSC403", title: "Computer Networks", units: 3 },
  { code: "CSC404", title: "Database Systems", units: 3 },
];

const notifications: NotificationData[] = [
  { id: "n1", title: "Course Registration", message: "Registration opens tomorrow", type: "info" },
  { id: "n2", title: "Exam Timetable", message: "Final exam timetable published", type: "success" },
  { id: "n3", title: "Fee Reminder", message: "Payment deadline in 5 days", type: "warning" },
];

function StatCard({ title, value, color }: { title: string; value: string; color: string }) {
  const bgColors: Record<string, string> = {
    blue: "#dbeafe",
    green: "#dcfce7",
    amber: "#fef3c7",
    indigo: "#e0e7ff",
  };

  return (
    <View style={[styles.statCard, { backgroundColor: bgColors[color] || "#f3f4f6" }]}>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statTitle}>{title}</Text>
    </View>
  );
}

function CourseItem({ course }: { course: Course }) {
  return (
    <View style={styles.courseItem}>
      <View>
        <Text style={styles.courseCode}>{course.code}</Text>
        <Text style={styles.courseTitle}>{course.title}</Text>
      </View>
      <Text style={styles.courseUnits}>{course.units} units</Text>
    </View>
  );
}

function NotificationCard({ notification }: { notification: NotificationData }) {
  const typeStyles: Record<string, { bg: string; text: string }> = {
    info: { bg: "#dbeafe", text: "#1e40af" },
    success: { bg: "#dcfce7", text: "#166534" },
    warning: { bg: "#fef3c7", text: "#92400e" },
  };

  const style = typeStyles[notification.type] || typeStyles.info;

  return (
    <View style={[styles.notification, { backgroundColor: style.bg }]}>
      <Text style={[styles.notificationTitle, { color: style.text }]}>{notification.title}</Text>
      <Text style={styles.notificationMessage}>{notification.message}</Text>
    </View>
  );
}

function QuickAction({ label, emoji }: { label: string; emoji: string }) {
  return (
    <TouchableOpacity style={styles.actionBtn}>
      <Text style={styles.actionEmoji}>{emoji}</Text>
      <Text style={styles.actionText}>{label}</Text>
    </TouchableOpacity>
  );
}

export default function HomeScreen() {
  const bottomNav = [
    { name: "Home", emoji: "🏠" },
    { name: "Courses", emoji: "📚" },
    { name: "Finance", emoji: "💳" },
    { name: "Profile", emoji: "👤" },
  ];

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scroll} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <View style={styles.logoContainer}>
            <Text style={styles.logoEmoji}>🎓</Text>
          </View>
          <View>
            <Text style={styles.welcomeText}>Welcome back!</Text>
            <Text style={styles.studentName}>{student.first_name}</Text>
          </View>
        </View>

        <View style={styles.statsGrid}>
          <StatCard title="GPA" value={student.gpa.toString()} color="blue" />
          <StatCard title="Courses" value="5" color="indigo" />
          <StatCard title="Attendance" value="94%" color="green" />
          <StatCard title="Credits" value="118" color="amber" />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Current Courses</Text>
          {courses.map((course) => (
            <CourseItem key={course.code} course={course} />
          ))}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Notifications</Text>
          {notifications.map((n) => (
            <NotificationCard key={n.id} notification={n} />
          ))}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <View style={styles.actionsGrid}>
            <QuickAction label="Register" emoji="📝" />
            <QuickAction label="Results" emoji="📊" />
            <QuickAction label="Pay Fees" emoji="💰" />
            <QuickAction label="Library" emoji="📚" />
          </View>
        </View>

        <View style={styles.bottomSpacer} />
      </ScrollView>

      <View style={styles.bottomNav}>
        {bottomNav.map((item) => (
          <TouchableOpacity key={item.name} style={styles.navItem}>
            <Text style={styles.navEmoji}>{item.emoji}</Text>
            <Text style={styles.navLabel}>{item.name}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f9fafb" },
  scroll: { flex: 1, padding: 16 },
  header: { flexDirection: "row", alignItems: "center", marginBottom: 20, gap: 12 },
  logoContainer: { width: 48, height: 48, borderRadius: 12, backgroundColor: "#2563eb", alignItems: "center", justifyContent: "center" },
  logoEmoji: { fontSize: 24 },
  welcomeText: { fontSize: 14, color: "#6b7280" },
  studentName: { fontSize: 20, fontWeight: "700", color: "#111827" },
  statsGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginBottom: 24 },
  statCard: { width: "47%", padding: 16, borderRadius: 16 },
  statValue: { fontSize: 24, fontWeight: "700", color: "#111827" },
  statTitle: { fontSize: 12, color: "#6b7280", marginTop: 4 },
  section: { marginBottom: 24 },
  sectionTitle: { fontSize: 18, fontWeight: "600", color: "#111827", marginBottom: 12 },
  courseItem: { backgroundColor: "#ffffff", padding: 16, borderRadius: 12, marginBottom: 8, flexDirection: "row", justifyContent: "space-between", alignItems: "center", shadowColor: "#000", shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1 },
  courseCode: { fontSize: 14, fontWeight: "600", color: "#2563eb" },
  courseTitle: { fontSize: 14, color: "#374151", marginTop: 2 },
  courseUnits: { fontSize: 12, color: "#6b7280" },
  notification: { padding: 14, borderRadius: 12, marginBottom: 8 },
  notificationTitle: { fontSize: 14, fontWeight: "600" },
  notificationMessage: { fontSize: 12, color: "#6b7280", marginTop: 2 },
  actionsGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12 },
  actionBtn: { width: "47%", backgroundColor: "#ffffff", padding: 16, borderRadius: 12, alignItems: "center", shadowColor: "#000", shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1 },
  actionEmoji: { fontSize: 24, marginBottom: 4 },
  actionText: { fontSize: 14, color: "#374151" },
  bottomSpacer: { height: 20 },
  bottomNav: { flexDirection: "row", backgroundColor: "#ffffff", borderTopWidth: 1, borderTopColor: "#e5e7eb", paddingVertical: 8, paddingHorizontal: 16 },
  navItem: { flex: 1, alignItems: "center", paddingVertical: 8 },
  navEmoji: { fontSize: 20 },
  navLabel: { fontSize: 10, color: "#6b7280", marginTop: 2 },
});
