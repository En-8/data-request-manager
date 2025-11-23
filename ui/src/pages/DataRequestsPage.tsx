import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { apiFetch } from '../lib/api'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Tabs,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { Spinner } from '@/components/ui/spinner'
import { type DataRequest, StatusLabels } from '../types/data-request'

export function DataRequestsPage() {
  const [dataRequests, setDataRequests] = useState<DataRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [status, setStatus] = useState('3') // Default to "Needs Review"

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setLoading(true)
    apiFetch(`/api/v1/data-requests?status=${status}`)
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
  }, [status])

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Data Requests</h1>
      <div className="flex items-center justify-between mb-4">
        <Tabs value={status} onValueChange={setStatus}>
          <TabsList>
            <TabsTrigger value="2">Processing</TabsTrigger>
            <TabsTrigger value="3">Needs Review</TabsTrigger>
            <TabsTrigger value="99">Complete</TabsTrigger>
          </TabsList>
        </Tabs>
        <Button asChild>
          <Link to="/data-requests/new">New Data Request</Link>
        </Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[8%]">ID</TableHead>
            <TableHead className="w-[20%]">Name</TableHead>
            <TableHead className="w-[12%]">Status</TableHead>
            <TableHead className="w-[15%]">Created On</TableHead>
            <TableHead className="w-[20%]">Created By</TableHead>
            <TableHead className="w-[25%]">Request Source ID</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {loading ? (
            <TableRow>
              <TableCell colSpan={6} className="text-center py-8">
                <Spinner className="size-6 mx-auto" />
              </TableCell>
            </TableRow>
          ) : (
            dataRequests.map((request) => (
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
            ))
          )}
        </TableBody>
      </Table>
    </div>
  )
}
