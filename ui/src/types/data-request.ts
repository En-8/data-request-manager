export interface DataRequest {
  id: number
  first_name: string
  last_name: string
  status: number
  created_on: string
  created_by: string
  request_source_id: string
}

export const StatusLabels: Record<number, string> = {
  1: 'Created',
  2: 'Processing',
  3: 'Needs Review',
  99: 'Complete',
}
