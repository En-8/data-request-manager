import { useContext } from 'react'
import { AuthContext } from './authContext'

export { AuthProvider } from './AuthContext'
export type { User, AuthContextType } from './authContext'

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
