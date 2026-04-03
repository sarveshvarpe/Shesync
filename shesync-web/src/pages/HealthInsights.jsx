import { useEffect, useState } from "react"
import api from "../api/api"
import { motion } from "framer-motion"
import DashboardLayout from "../layouts/DashboardLayout"

export default function HealthInsights() {

  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // NEW STATE
  const [downloading, setDownloading] = useState(false)

  useEffect(() => {

    const fetchData = async () => {

      try {

        const res = await api.get("/health/summary")

        setData(res.data)

      } catch (err) {

        console.error("Failed to load insights", err)
        setError("Unable to load health insights.")

      } finally {

        setLoading(false)

      }

    }

    fetchData()

  }, [])


  // ================= DOWNLOAD REPORT =================

  const downloadReport = async () => {

    try {

      setDownloading(true)

      const response = await api.get("/report/download", {
        responseType: "blob"
      })

      const url = window.URL.createObjectURL(
        new Blob([response.data])
      )

      const link = document.createElement("a")

      link.href = url
      link.setAttribute(
        "download",
        "shesync-ai-health-report.pdf"
      )

      document.body.appendChild(link)
      link.click()

    } catch (err) {

      console.error("Download failed:", err)
      alert("Failed to download report")

    } finally {

      setDownloading(false)

    }

  }


  if (loading) {

    return (
      <div className="flex items-center justify-center min-h-screen text-lg">
        Loading Health Insights...
      </div>
    )

  }

  if (error) {

    return (
      <div className="flex items-center justify-center min-h-screen text-red-500">
        {error}
      </div>
    )

  }

  if (!data) return null


  const predictionConfidence = data?.prediction?.prediction_confidence || "low"
  const dataConfidence = data?.confidence || "low"


  const confidenceWidth = (level) => {

    if (level === "high") return "85%"
    if (level === "moderate") return "60%"
    return "40%"

  }


  return (

    <DashboardLayout>

      {/* ================= HEADER ================= */}

      <div className="flex justify-between items-center mb-10">

        <h1 className="text-3xl font-bold dark:text-white">
          Advanced Health Intelligence
        </h1>

        {/* DOWNLOAD BUTTON */}

        <button
          onClick={downloadReport}
          disabled={downloading}
          className="bg-primary text-white px-6 py-3 rounded-xl hover:opacity-90 transition"
        >
          {downloading ? "Generating Report..." : "Download AI Health Report"}
        </button>

      </div>


      {/* ================= HEALTH ANALYTICS CARDS ================= */}

      <div className="grid md:grid-cols-3 gap-6 mb-10">

        <motion.div
          whileHover={{ scale: 1.05 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
        >

          <p className="text-sm text-gray-500 dark:text-gray-400">
            Cycle Health Score
          </p>

          <p className="text-3xl font-bold text-primary">
            {data.cycle_health_score}
          </p>

        </motion.div>


        <motion.div
          whileHover={{ scale: 1.05 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
        >

          <p className="text-sm text-gray-500 dark:text-gray-400">
            Hormonal Stability
          </p>

          <p className="text-3xl font-bold text-green-500">
            {data.hormonal_stability_index}
          </p>

        </motion.div>


        <motion.div
          whileHover={{ scale: 1.05 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
        >

          <p className="text-sm text-gray-500 dark:text-gray-400">
            Fertility Score
          </p>

          <p className="text-3xl font-bold text-indigo-500">
            {data.fertility_score}
          </p>

        </motion.div>

      </div>


      {/* ================= PCOS RISK CARD ================= */}

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft mb-8"
      >

        <h3 className="text-xl font-semibold mb-4 dark:text-white">
          PCOS Risk Analysis
        </h3>

        <div className="flex items-center justify-between">

          <p className="text-4xl font-bold text-primary">

            {data.pcos_risk_score
              ? (data.pcos_risk_score * 100).toFixed(0)
              : 0}%

          </p>


          <span
            className={`px-4 py-2 rounded-full text-sm capitalize font-medium
            ${
              data.pcos_risk_level === "low"
                ? "bg-green-100 text-green-600"
                : data.pcos_risk_level === "moderate"
                ? "bg-yellow-100 text-yellow-600"
                : "bg-red-100 text-red-600"
            }`}
          >

            {data.pcos_risk_level} Risk

          </span>

        </div>

      </motion.div>



      {/* ================= CONFIDENCE SECTION ================= */}

      <div className="grid md:grid-cols-2 gap-6 mb-8">


        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
        >

          <h4 className="font-semibold mb-3 dark:text-white">
            Prediction Confidence
          </h4>

          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">

            <div
              className="h-3 bg-primary rounded-full transition-all duration-700"
              style={{ width: confidenceWidth(predictionConfidence) }}
            />

          </div>

          <p className="mt-3 text-sm capitalize text-gray-500 dark:text-gray-400">
            {predictionConfidence}
          </p>

        </motion.div>



        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-soft"
        >

          <h4 className="font-semibold mb-3 dark:text-white">
            Data Confidence
          </h4>

          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">

            <div
              className="h-3 bg-green-500 rounded-full transition-all duration-700"
              style={{ width: confidenceWidth(dataConfidence) }}
            />

          </div>

          <p className="mt-3 text-sm capitalize text-gray-500 dark:text-gray-400">
            {dataConfidence}
          </p>

        </motion.div>

      </div>



      {/* ================= ALERTS ================= */}

      {data.alerts?.length > 0 && (

        <div className="mb-8">

          <h3 className="text-xl font-semibold mb-4 dark:text-white">
            Alerts
          </h3>

          {data.alerts.map((alert, index) => (

            <div
              key={index}
              className="bg-yellow-100 dark:bg-yellow-900
                         text-yellow-800 dark:text-yellow-200
                         p-4 rounded-lg mb-3"
            >

              {alert.message}

            </div>

          ))}

        </div>

      )}



      {/* ================= AI INSIGHTS ================= */}

      <div>

        <h3 className="text-xl font-semibold mb-6 dark:text-white">
          AI Clinical Insights
        </h3>

        <div className="space-y-4">

          {data.insights?.map((insight, index) => (

            <motion.div
              key={index}
              whileHover={{ scale: 1.02 }}
              className="bg-gradient-to-r
                         from-purple-50 to-indigo-50
                         dark:from-gray-800 dark:to-gray-700
                         p-5 rounded-xl shadow-sm"
            >

              <p className="dark:text-gray-200">
                {insight}
              </p>

            </motion.div>

          ))}

        </div>

      </div>

    </DashboardLayout>

  )

}