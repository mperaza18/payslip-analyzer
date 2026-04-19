import { useEffect, useState } from 'react'
import { fetchHealth, type HealthResponse } from '../api/client'

export default function HealthBadge() {
  const [data, setData] = useState<HealthResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchHealth()
      .then(setData)
      .catch((e: Error) => setError(e.message))
  }, [])

  if (error) {
    return (
      <span className="flex items-center gap-1.5 text-sm text-red-400">
        <span className="h-2 w-2 rounded-full bg-red-500" />
        Backend down: {error}
      </span>
    )
  }

  if (!data) {
    return (
      <span className="flex items-center gap-1.5 text-sm text-gray-400">
        <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400" />
        Connecting…
      </span>
    )
  }

  return (
    <span className="flex items-center gap-1.5 text-sm text-green-400">
      <span className="h-2 w-2 rounded-full bg-green-500" />
      <code className="text-xs">{JSON.stringify(data)}</code>
    </span>
  )
}
