import { useState } from "react"
import axios from "axios"
import DashboardLayout from "../layouts/DashboardLayout"

export default function Profile() {
  const [age, setAge] = useState("")
  const token = localStorage.getItem("token")

  const handleUpdate = async () => {
    await axios.put(
      "http://127.0.0.1:8000/user/update",
      { age: parseInt(age) },
      { headers: { Authorization: `Bearer ${token}` } }
    )

    alert("Profile updated")
  }

  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold mb-8">
        Profile Settings
      </h1>

      <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-soft max-w-xl">
        <input
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          placeholder="Enter your age"
          className="w-full p-3 rounded-xl border dark:border-gray-600 bg-transparent mb-4"
        />

        <button
          onClick={handleUpdate}
          className="w-full bg-primary text-white py-3 rounded-xl"
        >
          Update Age
        </button>
      </div>
    </DashboardLayout>
  )
}