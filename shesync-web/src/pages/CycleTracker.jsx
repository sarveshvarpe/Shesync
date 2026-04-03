import { useEffect, useState } from "react"
import api from "../api/api"
import Calendar from "react-calendar"
import "../styles/calendar.css"
import DashboardLayout from "../layouts/DashboardLayout"
import HealthAnalyticsChart from "../components/HealthAnalyticsChart"
import { motion } from "framer-motion"

export default function CycleTracker() {

  const [selectedDate, setSelectedDate] = useState(new Date())
  const [periodDate, setPeriodDate] = useState("")
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  // NEW STATE
  const [history, setHistory] = useState([])

  useEffect(() => {
    fetchHealthData()
    fetchCycleHistory()
  }, [])

  const fetchHealthData = async () => {
    try {
      const res = await api.get("/health/summary")
      setData(res.data)
    } catch (err) {
      console.error("Health summary failed:", err.response?.data || err.message)
    } finally {
      setLoading(false)
    }
  }

  // NEW FUNCTION
  const fetchCycleHistory = async () => {
    try {
      const res = await api.get("/cycle/history")
      setHistory(res.data)
    } catch (err) {
      console.error("Cycle history failed:", err.response?.data || err.message)
    }
  }

  const handleAddPeriod = async () => {
    if (!periodDate) {
      alert("Please select a date")
      return
    }
    console.log("Sending date:", periodDate)

    try {

      await api.post("/cycle/start", {
        start_date: periodDate
      })

      alert("Cycle started successfully")

      setPeriodDate("")
      fetchHealthData()
      fetchCycleHistory()   // NEW REFRESH

    } catch (err) {
      console.error("Failed to start cycle:", err.response?.data || err.message)
      alert("Failed to start cycle")
    }
  }

  const isDateInRange = (date, start, end) => {
    return date >= new Date(start) && date <= new Date(end)
  }

  const prediction = data?.prediction ?? {}
  const phase = data?.hormonal_phase ?? {}
  const trend = data?.trend_analysis ?? {}
  const recommendations = data?.recommendations ?? []

  const calculateDaysLeft = () => {
    if (!prediction?.next_period_date) return null

    const today = new Date()
    const nextDate = new Date(prediction.next_period_date)

    const diffTime = nextDate - today
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    return diffDays
  }

  const daysLeft = calculateDaysLeft()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen dark:text-white">
        Loading Cycle Intelligence...
      </div>
    )
  }

  if (!data) return null

  return (
    <DashboardLayout>

      <h1 className="text-3xl font-bold mb-10 dark:text-white">
        Reproductive Intelligence
      </h1>

      {/* ================= Countdown Card ================= */}

      {daysLeft !== null && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-10 p-6 bg-gradient-to-r from-pink-500 to-red-500 text-white rounded-3xl shadow-soft"
        >
          <h2 className="text-lg font-semibold">
            Next Period
          </h2>

          <p className="text-3xl font-bold mt-2">
            {daysLeft > 0
              ? `In ${daysLeft} days`
              : daysLeft === 0
              ? "Expected Today"
              : "Delayed"}
          </p>
        </motion.div>
      )}

      {/* ================= Score Cards ================= */}

      <div className="grid md:grid-cols-3 gap-6 mb-10">

        <motion.div whileHover={{ scale: 1.05 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Cycle Health Score
          </p>
          <p className="text-3xl font-bold text-primary">
            {data.cycle_health_score}
          </p>
        </motion.div>

        <motion.div whileHover={{ scale: 1.05 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Hormonal Stability
          </p>
          <p className="text-3xl font-bold text-green-500">
            {data.hormonal_stability_index}
          </p>
        </motion.div>

        <motion.div whileHover={{ scale: 1.05 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Fertility Score
          </p>
          <p className="text-3xl font-bold text-indigo-500">
            {data.fertility_score}
          </p>
        </motion.div>

      </div>

      {/* ================= Calendar & Chart ================= */}

      <div className="grid lg:grid-cols-3 gap-10">

        <div className="lg:col-span-2">
          <HealthAnalyticsChart data={data} />
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-soft"
        >
          <Calendar
            onChange={setSelectedDate}
            value={selectedDate}
            tileClassName={({ date }) => {

              const formatted = date.toISOString().split("T")[0]

              if (prediction?.next_period_date) {
                if (formatted === prediction.next_period_date) {
                  return "predicted-period-day"
                }
              }

              if (prediction?.ovulation_window_start) {
                if (
                  isDateInRange(
                    date,
                    prediction.ovulation_window_start,
                    prediction.ovulation_window_end
                  )
                ) {
                  return "ovulation-day"
                }
              }

              return null
            }}
          />
        </motion.div>

      </div>

      {/* ================= Lower Section ================= */}

      <div className="grid md:grid-cols-3 gap-8 mt-12">

        <div className="bg-gradient-to-r from-purple-500 to-indigo-500 text-white p-6 rounded-3xl shadow-soft">
          <h3 className="text-xl font-semibold mb-3">
            Current Phase
          </h3>
          <p className="text-2xl font-bold capitalize">
            {phase?.current_phase || "—"}
          </p>
          <p>Day {phase?.phase_day ?? "—"}</p>
          <p className="text-sm opacity-80 capitalize">
            Stability: {phase?.phase_stability || "—"}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-soft">
          <h3 className="font-semibold mb-4 dark:text-white">
            Trend Analysis
          </h3>

          <div className="space-y-2 text-sm dark:text-gray-300">
            <p>Cycle Shift: {trend?.cycle_length_shift || "—"}</p>
            <p>Variability Trend: {trend?.variability_trend || "—"}</p>
            <p>Symptom Trend: {trend?.symptom_intensity_trend || "—"}</p>
            <p>Risk Direction: {trend?.risk_direction || "—"}</p>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-soft">
          <h3 className="font-semibold mb-4 dark:text-white">
            Start New Cycle
          </h3>

          <input
            type="date"
            value={periodDate}
            onChange={(e) => setPeriodDate(e.target.value)}
            className="w-full p-3 border rounded-xl mb-4 bg-transparent dark:border-gray-600 dark:text-white"
          />

          <button
            onClick={handleAddPeriod}
            className="w-full bg-primary text-white py-3 rounded-xl hover:opacity-90 transition"
          >
            Start Cycle
          </button>
        </div>

      </div>

      {/* ================= Recommendations ================= */}

      <div className="mt-12">
        <h2 className="text-2xl font-semibold mb-6 dark:text-white">
          Personalized Recommendations
        </h2>

        <div className="grid md:grid-cols-2 gap-6">
          {recommendations.map((rec, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.02 }}
              className="bg-indigo-50 dark:bg-gray-800 p-5 rounded-xl shadow-sm dark:text-white"
            >
              {rec}
            </motion.div>
          ))}
        </div>
      </div>

      {/* ================= Cycle History ================= */}

      <div className="mt-16">

        <h2 className="text-2xl font-semibold mb-6 dark:text-white">
          Cycle History
        </h2>

        <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-soft overflow-hidden">

          <table className="w-full text-sm">

            <thead className="bg-gray-100 dark:bg-gray-700">
              <tr>
                <th className="p-4 text-left">Start Date</th>
                <th className="p-4 text-left">End Date</th>
                <th className="p-4 text-left">Cycle Length</th>
              </tr>
            </thead>

            <tbody>

              {history.length === 0 && (
                <tr>
                  <td colSpan="3" className="p-4 text-center text-gray-500">
                    No cycle history available
                  </td>
                </tr>
              )}

              {history.map((cycle, index) => {

                const start = new Date(cycle.start_date)
                const end = cycle.end_date ? new Date(cycle.end_date) : null

                const length =
                  end
                    ? Math.round((end - start) / (1000 * 60 * 60 * 24))
                    : null

                return (

                  <tr key={index} className="border-t dark:border-gray-700">

                    <td className="p-4">{cycle.start_date}</td>

                    <td className="p-4">
                      {cycle.end_date || "Active"}
                    </td>

                    <td className="p-4">
                      {length ? `${length} days` : "-"}
                    </td>

                  </tr>

                )
              })}

            </tbody>

          </table>

        </div>

      </div>

    </DashboardLayout>
  )
}