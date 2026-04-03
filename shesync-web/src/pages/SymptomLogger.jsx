import { useState } from "react"
import api from "../api/api"
import DashboardLayout from "../layouts/DashboardLayout"
import { motion } from "framer-motion"

export default function SymptomLogger() {

  const [form, setForm] = useState({
    acne: false,
    severe_pms: false,
    heavy_bleeding: false,
    weight_instability: false,
    mood_swings: false
  })

  const handleChange = (e) => {
    const { name, checked } = e.target
    setForm({
      ...form,
      [name]: checked
    })
  }

  const handleSubmit = async () => {
    try {
      await api.post("/cycle/log", form)

      alert("Symptoms logged successfully")

      setForm({
        acne: false,
        severe_pms: false,
        heavy_bleeding: false,
        weight_instability: false,
        mood_swings: false
      })

    } catch (err) {
      console.error(err.response?.data || err.message)
      alert("Failed to log symptoms")
    }
  }

  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold mb-8 dark:text-white">
        Daily Symptom Logger
      </h1>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white dark:bg-gray-800 p-8 rounded-3xl shadow-soft"
      >
        <div className="space-y-4">

          {Object.keys(form).map((key) => (
            <label
              key={key}
              className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-xl cursor-pointer"
            >
              <span className="capitalize dark:text-white">
                {key.replace("_", " ")}
              </span>

              <input
                type="checkbox"
                name={key}
                checked={form[key]}
                onChange={handleChange}
                className="w-5 h-5 accent-primary"
              />
            </label>
          ))}

          <button
            onClick={handleSubmit}
            className="w-full mt-6 bg-primary text-white py-3 rounded-xl hover:opacity-90 transition"
          >
            Save Symptoms
          </button>

        </div>
      </motion.div>

    </DashboardLayout>
  )
}