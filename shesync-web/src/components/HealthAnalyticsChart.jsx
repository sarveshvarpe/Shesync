import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts"

function HealthAnalyticsChart({ data }) {

  if (!data) return null

  const chartData = [
    {
      name: "Overview",
      score: data?.cycle_health_score || 0,
      stability: data?.hormonal_stability_index || 0,
      fertility: data?.fertility_score || 0
    }
  ]

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-soft">
      <h3 className="text-lg font-semibold mb-4 dark:text-white">
        Health Analytics Overview
      </h3>

      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Line type="monotone" dataKey="score" stroke="#7C3AED" strokeWidth={3} />
            <Line type="monotone" dataKey="stability" stroke="#10B981" strokeWidth={3} />
            <Line type="monotone" dataKey="fertility" stroke="#6366F1" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default HealthAnalyticsChart