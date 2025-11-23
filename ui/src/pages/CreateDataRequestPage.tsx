import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router'
import { apiFetch } from '../lib/api'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

interface RequestSource {
  id: string
  name: string
}

interface Person {
  id: number
  first_name: string
  last_name: string
  date_of_birth: string
}

export function CreateDataRequestPage() {
  const navigate = useNavigate()
  const [requestSources, setRequestSources] = useState<RequestSource[]>([])
  const [people, setPeople] = useState<Person[]>([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [personId, setPersonId] = useState('')
  const [requestSourceId, setRequestSourceId] = useState('')

  useEffect(() => {
    Promise.all([
      apiFetch('/api/v1/request-sources').then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch request sources')
        }
        return response.json()
      }),
      apiFetch('/api/v1/people').then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch people')
        }
        return response.json()
      }),
    ])
      .then(([requestSourcesData, peopleData]) => {
        setRequestSources(requestSourcesData)
        setPeople(peopleData)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setError(null)

    try {
      const response = await apiFetch('/api/v1/data-requests', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          person_id: parseInt(personId, 10),
          request_source_id: requestSourceId,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to create data request')
      }

      navigate('/')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="p-4">Loading...</div>
  }

  return (
    <div className="p-4 max-w-md">
      <h1 className="text-2xl font-bold mb-4">New Data Request</h1>
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="person">Person</Label>
          <Select value={personId} onValueChange={setPersonId} required>
            <SelectTrigger>
              <SelectValue placeholder="Select a person" />
            </SelectTrigger>
            <SelectContent>
              {people.map((person) => (
                <SelectItem key={person.id} value={String(person.id)}>
                  {person.first_name} {person.last_name} ({person.date_of_birth})
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <Label htmlFor="requestSource">Request Source</Label>
          <Select value={requestSourceId} onValueChange={setRequestSourceId} required>
            <SelectTrigger>
              <SelectValue placeholder="Select a request source" />
            </SelectTrigger>
            <SelectContent>
              {requestSources.map((source) => (
                <SelectItem key={source.id} value={source.id}>
                  {source.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex gap-2 pt-4">
          <Button type="submit" disabled={submitting || !personId || !requestSourceId}>
            {submitting ? 'Creating...' : 'Create'}
          </Button>
          <Button type="button" variant="outline" asChild>
            <Link to="/">Cancel</Link>
          </Button>
        </div>
      </form>
    </div>
  )
}
