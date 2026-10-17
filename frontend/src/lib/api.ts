const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8080'

export async function getBackendHealth(): Promise<{ status: string; service: string }> {
  const response = await fetch(`${apiBaseUrl}/health`)
  if (!response.ok) throw new Error('Backend health check failed')
  return response.json() as Promise<{ status: string; service: string }>
}
