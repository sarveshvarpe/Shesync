import { NavLink, useNavigate } from "react-router-dom"
import {
  LayoutDashboard,
  Activity,
  CalendarDays,
  Stethoscope,
  User,
  LogOut
} from "lucide-react"

import useDarkMode from "../hooks/useDarkMode"
import Chatbot from "../components/Chatbot"

export default function DashboardLayout({ children }) {

  const navigate = useNavigate()
  const [theme, setTheme] = useDarkMode()

  const handleLogout = () => {
    localStorage.removeItem("token")
    navigate("/login")
  }

  const navItemClass = ({ isActive }) =>
    `flex items-center gap-3 p-3 rounded-xl transition-all duration-200
     ${
       isActive
         ? "bg-primary text-white shadow-md"
         : "hover:bg-gray-100 dark:hover:bg-gray-700"
     }`

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-white transition-colors duration-300">

      {/* ================= SIDEBAR ================= */}
      <aside className="w-64 fixed left-0 top-0 h-full bg-white dark:bg-gray-800 shadow-soft flex flex-col justify-between p-6">

        {/* Top */}
        <div>

          {/* Logo */}
          <h1 className="text-2xl font-bold text-primary mb-10">
            SheSync
          </h1>

          {/* Navigation */}
          <nav className="space-y-3">

            <NavLink to="/dashboard" className={navItemClass}>
              <LayoutDashboard size={18} />
              Dashboard
            </NavLink>

            <NavLink to="/insights" className={navItemClass}>
              <Activity size={18} />
              Health Insights
            </NavLink>

            <NavLink to="/cycle" className={navItemClass}>
              <CalendarDays size={18} />
              Cycle Tracker
            </NavLink>

            <NavLink to="/symptoms" className={navItemClass}>
              <Stethoscope size={18} />
              Symptom Logger
            </NavLink>

            <NavLink to="/profile" className={navItemClass}>
              <User size={18} />
              Profile
            </NavLink>

          </nav>
        </div>

        {/* Bottom */}
        <div className="space-y-4">

          {/* Dark Mode Toggle */}
          <button
            onClick={() =>
              setTheme(theme === "dark" ? "light" : "dark")
            }
            className="w-full px-4 py-2 rounded-xl bg-primary text-white text-sm hover:opacity-90 transition"
          >
            {theme === "dark" ? "☀ Light Mode" : "🌙 Dark Mode"}
          </button>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full p-3 rounded-xl hover:bg-red-100 dark:hover:bg-red-900 text-red-500 transition"
          >
            <LogOut size={18} />
            Logout
          </button>

        </div>

      </aside>

      {/* ================= MAIN CONTENT ================= */}
      <main className="flex-1 ml-64 p-10 overflow-y-auto">
        {children}
      </main>

      {/* ================= GLOBAL CHATBOT ================= */}
      <Chatbot />

    </div>
  )
}