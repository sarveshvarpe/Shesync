import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts"
import { motion } from "framer-motion"

export default function HealthTrendChart({ score }) {
  // Mock dynamic data (later we can connect backend trend history)
  const data = [
    { name: "Cycle 1", value: score - 8 },
    { name: "Cycle 2", value: score - 4 },
    { name: "Cycle 3", value: score - 2 },
    { name: "Cycle 4", value: score },
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-white p-6 rounded-2xl shadow-soft mt-10"
    >
      <h3 className="text-xl font-semibold mb-4">
        Hormonal Stability Trend
      </h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#7C3AED"
            strokeWidth={3}
            dot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  )
}