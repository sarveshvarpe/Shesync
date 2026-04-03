import { useState } from "react"
import axios from "axios"
import { motion } from "framer-motion"
import { useNavigate } from "react-router-dom"

export default function VerifyOTP() {
  const navigate = useNavigate()

  const email = localStorage.getItem("verify_email")

  const [otp, setOtp] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    try {
      await axios.post(
        "http://127.0.0.1:8000/auth/verify-otp",
        {
          email,
          otp,
        }
      )

      setSuccess("Account verified successfully!")

      localStorage.removeItem("verify_email")

      setTimeout(() => {
        navigate("/login")
      }, 1500)

    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Invalid or expired OTP"
      )
    }

    setLoading(false)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-600 to-indigo-600">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white p-8 rounded-3xl shadow-2xl w-96"
      >
        <h2 className="text-2xl font-bold mb-6 text-center">
          Verify OTP
        </h2>

        <p className="text-sm text-gray-500 mb-4 text-center">
          OTP sent to {email}
        </p>

        {error && (
          <p className="text-red-500 text-sm mb-4 text-center">
            {error}
          </p>
        )}

        {success && (
          <p className="text-green-600 text-sm mb-4 text-center">
            {success}
          </p>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            type="text"
            placeholder="Enter OTP"
            required
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            className="w-full p-3 border rounded-lg text-center tracking-widest text-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-3 rounded-lg hover:opacity-90 transition"
          >
            {loading ? "Verifying..." : "Verify"}
          </button>
        </form>
      </motion.div>
    </div>
  )
}