import { motion } from "framer-motion"
import { HeartPulse } from "lucide-react"
import { useNavigate } from "react-router-dom"

export default function Landing() {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-primary to-secondary text-white text-center px-6">
      
      {/* Animated Logo */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5 }}
        className="mb-6"
      >
        <HeartPulse size={70} />
      </motion.div>

      {/* Title */}
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="text-5xl font-bold"
      >
        SheSync
      </motion.h1>

      {/* Subtitle */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="mt-4 text-lg text-purple-100 max-w-xl"
      >
        AI-Powered Reproductive Intelligence  
        Track. Predict. Understand.
      </motion.p>

      {/* CTA Button */}
      <motion.button
        whileHover={{ scale: 1.07 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => navigate("/login")}
        className="mt-10 px-8 py-3 bg-white text-primary font-semibold rounded-xl shadow-soft hover:shadow-lg transition duration-300"
      >
        Get Started
      </motion.button>

    </div>
  )
}