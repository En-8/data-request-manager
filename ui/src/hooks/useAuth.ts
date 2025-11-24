import { useContext } from 'react'
import { AuthContext } from './authContext.ts'
export { AuthProvider } from './AuthContext.tsx'
export type { User, AuthContextType } from './AuthContext.tsx'

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
