import { motion } from "framer-motion"

export default function MainLayout({ children }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary to-secondary">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="p-8"
      >
        {children}
      </motion.div>
    </div>
  )
}