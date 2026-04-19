const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export interface HealthResponse {
  status: string
  llm_provider: string
}

export const fetchHealth = (signal?: AbortSignal): Promise<HealthResponse> =>
  fetch(`${BASE_URL}/health`, { signal }).then((r) => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    return r.json()
  })

// TODO: add runtime shape validation (zod) before Phase 3 response handling
