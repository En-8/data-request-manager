import { Routes, Route } from 'react-router'
import { DataRequestsPage } from './pages/DataRequestsPage'
import { CreateDataRequestPage } from './pages/CreateDataRequestPage'
import { LoginPage } from './pages/LoginPage'
import { LogoutPage } from './pages/LogoutPage'
import { ProtectedRoute } from './components/ProtectedRoute'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/logout" element={<LogoutPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <DataRequestsPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/data-requests/new"
        element={
          <ProtectedRoute>
            <CreateDataRequestPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

export default App
