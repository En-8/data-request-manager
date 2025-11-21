import { useEffect, useState } from 'react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { DataRequest, StatusLabels } from './types/data-request'
import './App.css'

function App() {
  const [dataRequests, setDataRequests] = useState<DataRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/data-requests')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch data requests')
        }
        return response.json()
      })
      .then((data) => {
        setDataRequests(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="p-4">Loading...</div>
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Data Requests</h1>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Created On</TableHead>
            <TableHead>Created By</TableHead>
            <TableHead>Request Source ID</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {dataRequests.map((request) => (
            <TableRow key={request.id}>
              <TableCell>{request.id}</TableCell>
              <TableCell>
                {request.first_name} {request.last_name}
              </TableCell>
              <TableCell>{StatusLabels[request.status] ?? request.status}</TableCell>
              <TableCell>
                {new Date(request.created_on).toLocaleDateString()}
              </TableCell>
              <TableCell>{request.created_by}</TableCell>
              <TableCell>{request.request_source_id}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

export default App
