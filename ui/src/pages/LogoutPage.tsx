import { useEffect } from 'react'
import { useNavigate } from 'react-router'
import { useAuth } from '../hooks/useAuth'
import { Spinner } from '../components/ui/spinner'

export function LogoutPage() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    logout().then(() => {
      navigate('/login')
    })
  }, [logout, navigate])

  return (
    <div className="flex min-h-screen items-center justify-center">
      <Spinner className="size-8" />
    </div>
  )
}
