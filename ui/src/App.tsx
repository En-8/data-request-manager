import { Routes, Route } from 'react-router'
import { DataRequestsPage } from './pages/DataRequestsPage'
import { CreateDataRequestPage } from './pages/CreateDataRequestPage'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<DataRequestsPage />} />
      <Route path="/data-requests/new" element={<CreateDataRequestPage />} />
    </Routes>
  )
}

export default App
