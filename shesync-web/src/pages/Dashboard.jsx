import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import DashboardLayout from "../layouts/DashboardLayout"
import api from "../api/api"

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHealthData()
  }, [])

  const fetchHealthData = async () => {
    try {
      const res = await api.get("/health/summary")
      setData(res.data)
    } catch (error) {
      console.error("Failed to fetch dashboard data", error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        Loading health intelligence...
      </div>
    )
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        No data available.
      </div>
    )
  }

  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold mb-10">
        Health Overview
      </h1>

      {/* SCORE CARDS */}
      <div className="grid md:grid-cols-3 gap-6 mb-10">
        <ScoreCard title="Cycle Health" value={data.cycle_health_score} />
        <ScoreCard title="Hormonal Stability" value={data.hormonal_stability_index} />
        <ScoreCard title="Fertility Score" value={data.fertility_score} />
      </div>

      {/* PREDICTION + PHASE */}
      <div className="grid md:grid-cols-2 gap-6 mb-10">

        {/* Prediction */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-soft"
        >
          <h3 className="text-xl font-semibold mb-4">
            Cycle Prediction
          </h3>

          <div className="space-y-2">
            <p><strong>Next Period:</strong> {data.prediction.next_period_date}</p>
            <p>
              <strong>Ovulation Window:</strong>{" "}
              {data.prediction.ovulation_window_start} →{" "}
              {data.prediction.ovulation_window_end}
            </p>
            <p>
              <strong>Confidence:</strong>{" "}
              <span className="capitalize text-primary font-semibold">
                {data.prediction.prediction_confidence}
              </span>
            </p>
          </div>
        </motion.div>

        {/* Hormonal Phase */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-soft"
        >
          <h3 className="text-xl font-semibold mb-4">
            Current Phase
          </h3>

          <p className="text-2xl font-bold capitalize text-primary">
            {data.hormonal_phase.current_phase}
          </p>

          <p>Day {data.hormonal_phase.phase_day}</p>
          <p className="text-sm capitalize opacity-70">
            Stability: {data.hormonal_phase.phase_stability}
          </p>
        </motion.div>

      </div>

      {/* AI INSIGHTS */}
      <div>
        <h3 className="text-2xl font-bold mb-6">
          AI Clinical Insights
        </h3>

        <div className="grid md:grid-cols-2 gap-6">
          {data.insights.map((insight, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.02 }}
              className="bg-gradient-to-r from-purple-50 to-indigo-50 
                         dark:from-gray-800 dark:to-gray-700 
                         p-5 rounded-2xl shadow-sm"
            >
              {insight}
            </motion.div>
          ))}
        </div>
      </div>

    </DashboardLayout>
  )
}

/* SCORE CARD COMPONENT */
function ScoreCard({ title, value }) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-soft text-center"
    >
      <h3 className="text-gray-500 dark:text-gray-400 mb-4">
        {title}
      </h3>

      <p className="text-4xl font-bold text-primary">
        {value}
      </p>
    </motion.div>
  )
}