import { BrowserRouter as Router, Routes, Route } from "react-router-dom"

import Landing from "./pages/Landing"
import Login from "./pages/Login"
import Signup from "./pages/Signup"
import VerifyOTP from "./pages/VerifyOTP"
import Dashboard from "./pages/Dashboard"
import HealthInsights from "./pages/HealthInsights"
import CycleTracker from "./pages/CycleTracker"
import SymptomLogger from "./pages/SymptomLogger"
import Profile from "./pages/Profile"


import ProtectedRoute from "./components/ProtectedRoute"

function App() {
  return (
    <Router>
      <Routes>

        {/* Public Routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/verify-otp" element={<VerifyOTP />} />
        <Route path="/insights" element={<HealthInsights />} />
        <Route path="/cycle" element={<CycleTracker />} />
        <Route path="/symptoms" element={<ProtectedRoute><SymptomLogger /></ProtectedRoute>} /> 
        <Route path="/profile" element={<Profile />}/>


        {/* Protected Route */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

      </Routes>
    </Router>
  )
}

export default App