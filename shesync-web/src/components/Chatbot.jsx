import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import api from "../api/api"

export default function Chatbot() {

  const [open, setOpen] = useState(false)
  const [input, setInput] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const chatEndRef = useRef(null)

  const suggestions = [
    "When is my next period?",
    "Am I fertile today?",
    "What is my PCOS risk?",
    "Why is my cycle irregular?"
  ]

  // Auto scroll to newest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const getTime = () => {
    const now = new Date()
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  const sendMessage = async (messageText = input) => {

    if (!messageText.trim()) return

    const userMessage = {
      role: "user",
      content: messageText,
      time: getTime()
    }

    setMessages(prev => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {

      const res = await api.post("/chat/", {
        message: messageText
      })

      const botMessage = {
        role: "assistant",
        content: res.data.reply,
        health_score: res.data.health_score,
        risk_summary: res.data.risk_summary,
        alerts: res.data.alerts,
        time: getTime()
      }

      setMessages(prev => [...prev, botMessage])

    } catch (err) {

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ AI service unavailable. Please try again.",
          time: getTime()
        }
      ])

    }

    setLoading(false)
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage()
  }

  return (
    <>
      {/* Floating AI Button with Pulse Animation */}
      <motion.button
        animate={{
          scale: [1, 1.08, 1]
        }}
        transition={{
          duration: 2,
          repeat: Infinity
        }}
        whileHover={{ scale: 1.15 }}
        onClick={() => setOpen(!open)}
        className="fixed bottom-6 right-6 bg-pink-500 text-white p-4 rounded-full shadow-xl z-50"
      >
        🤖
      </motion.button>


      <AnimatePresence>

        {open && (

          <motion.div
            initial={{ opacity: 0, y: 80 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 80 }}
            className="fixed bottom-20 right-6 w-96 bg-white dark:bg-gray-900 shadow-2xl rounded-3xl flex flex-col overflow-hidden z-50"
          >

            {/* Header */}
            <div className="bg-gradient-to-r from-pink-500 to-purple-500 text-white p-4 font-semibold">
              SheSync AI Doctor
            </div>


            {/* Messages */}
            <div className="flex-1 p-4 space-y-4 overflow-y-auto max-h-96">

              {messages.length === 0 && (

                <div className="space-y-2">

                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Ask me about your cycle health
                  </p>

                  <div className="flex flex-wrap gap-2">

                    {suggestions.map((s, i) => (

                      <button
                        key={i}
                        onClick={() => sendMessage(s)}
                        className="text-xs bg-pink-100 dark:bg-gray-700 px-3 py-1 rounded-full"
                      >
                        {s}
                      </button>

                    ))}

                  </div>

                </div>

              )}

              {messages.map((msg, index) => (

                <div key={index}>

                  {/* USER MESSAGE */}
                  {msg.role === "user" && (

                    <div className="flex justify-end">

                      <motion.div
                        initial={{ scale: 0.9 }}
                        animate={{ scale: 1 }}
                        className="bg-pink-500 text-white px-4 py-2 rounded-2xl max-w-xs"
                      >
                        <p>{msg.content}</p>
                        <span className="text-[10px] opacity-70">
                          {msg.time}
                        </span>
                      </motion.div>

                    </div>

                  )}


                  {/* AI MESSAGE */}
                  {msg.role === "assistant" && (

                    <div className="flex gap-2 max-w-xs">

                      {/* Doctor Avatar */}
                      <div className="bg-pink-500 text-white p-2 rounded-full h-fit">
                        👩‍⚕️
                      </div>

                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="bg-gray-100 dark:bg-gray-800 p-3 rounded-2xl text-sm dark:text-white space-y-2"
                      >

                        <p>{msg.content}</p>

                        {/* Health Score */}
                        {msg.health_score && (

                          <div className="text-xs bg-white dark:bg-gray-700 p-2 rounded-lg">
                            Health Score: {msg.health_score}
                          </div>

                        )}

                        {/* PCOS Risk */}
                        {msg.risk_summary && (

                          <div className="text-xs bg-pink-50 dark:bg-gray-700 p-2 rounded-lg">
                            PCOS Risk: {msg.risk_summary.risk_level}
                          </div>

                        )}

                        {/* Alerts */}
                        {msg.alerts && msg.alerts.length > 0 && (

                          <div className="text-xs text-red-500">

                            {msg.alerts.map((alert, i) => (

                              <div key={i}>⚠️ {alert.message}</div>

                            ))}

                          </div>

                        )}

                        <span className="text-[10px] opacity-60">
                          {msg.time}
                        </span>

                      </motion.div>

                    </div>

                  )}

                </div>

              ))}

              {loading && (
                <div className="text-sm text-gray-400">
                  AI is thinking...
                </div>
              )}

              <div ref={chatEndRef} />

            </div>


            {/* Input */}
            <div className="p-3 border-t dark:border-gray-700 flex gap-2">

              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Ask about your cycle..."
                className="flex-1 p-2 rounded-lg border dark:bg-gray-800 dark:border-gray-600 text-sm"
              />

              <button
                onClick={() => sendMessage()}
                className="bg-pink-500 text-white px-4 rounded-lg text-sm"
              >
                Send
              </button>

            </div>

          </motion.div>

        )}

      </AnimatePresence>
    </>
  )
}