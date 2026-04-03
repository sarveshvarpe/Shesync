import { useState } from "react"
import axios from "axios"
import { motion } from "framer-motion"
import { Link, useNavigate } from "react-router-dom"

export default function Signup() {
  const navigate = useNavigate()

  const [form, setForm] = useState({
    name: "",
    age: "",
    email: "",
    password: "",
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    try {
      await axios.post(
        "http://127.0.0.1:8000/auth/signup",
        {
          name: form.name,
          age: Number(form.age),
          email: form.email,
          password: form.password,
        }
      )

      // Save email temporarily for OTP verification
      localStorage.setItem("verify_email", form.email)

      // Redirect to OTP page
      navigate("/verify-otp")

    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Signup failed. Please try again."
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
          Create Account
        </h2>

        {error && (
          <p className="text-red-500 text-sm mb-4 text-center">
            {error}
          </p>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            type="text"
            name="name"
            placeholder="Full Name"
            required
            onChange={handleChange}
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />

          <input
            type="number"
            name="age"
            placeholder="Age"
            required
            onChange={handleChange}
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />

          <input
            type="email"
            name="email"
            placeholder="Email"
            required
            onChange={handleChange}
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            required
            onChange={handleChange}
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-3 rounded-lg hover:opacity-90 transition"
          >
            {loading ? "Creating..." : "Sign Up"}
          </button>
        </form>

        <p className="text-sm text-center mt-6">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-purple-600 font-semibold hover:underline"
          >
            Login
          </Link>
        </p>
      </motion.div>
    </div>
  )
}