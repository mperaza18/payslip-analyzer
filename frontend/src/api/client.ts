const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export interface HealthResponse {
  status: string
  llm_provider: string
}

export const fetchHealth = (): Promise<HealthResponse> =>
  fetch(`${BASE_URL}/health`).then((r) => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    return r.json()
  })
