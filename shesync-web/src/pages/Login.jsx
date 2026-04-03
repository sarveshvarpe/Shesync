import { useState } from "react"
import { motion } from "framer-motion"
import { Link, useNavigate } from "react-router-dom"
import api from "../api/api"

export default function Login() {

  const navigate = useNavigate()

  const [form, setForm] = useState({
    email: "",
    password: ""
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleChange = (e) => {

    setForm({
      ...form,
      [e.target.name]: e.target.value
    })

  }

  const handleSubmit = async (e) => {

    e.preventDefault()

    setLoading(true)
    setError("")

    try {

      const res = await api.post(
        "/auth/login",
        {
          email: form.email,
          password: form.password
        }
      )

      localStorage.setItem(
        "token",
        res.data.access_token
      )

      localStorage.setItem(
        "refresh_token",
        res.data.refresh_token
      )

      navigate("/dashboard")

    } catch (err) {

      console.error(err.response?.data)

      setError(
        err.response?.data?.detail ||
        "Invalid credentials"
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
          Login
        </h2>

        {error && (
          <p className="text-red-500 text-sm mb-4 text-center">
            {error}
          </p>
        )}

        <form
          onSubmit={handleSubmit}
          className="space-y-4"
        >

          <input
            type="email"
            name="email"
            placeholder="Email"
            required
            value={form.email}
            onChange={handleChange}
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            required
            value={form.password}
            onChange={handleChange}
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white py-3 rounded-lg hover:opacity-90 transition"
          >

            {loading ? "Logging in..." : "Login"}

          </button>

        </form>

        <p className="text-sm text-center mt-6">

          Don’t have an account?{" "}

          <Link
            to="/signup"
            className="text-purple-600 font-semibold hover:underline"
          >
            Sign Up
          </Link>

        </p>

      </motion.div>

    </div>

  )

}