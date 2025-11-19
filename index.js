import useSWR from 'swr'
const fetcher = (url) => fetch(url).then(r => r.json())

export default function Home(){
  const {data: locs} = useSWR('/api/locations', fetcher)
  const apiRoot = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8000'
  const {data: apiLocs} = useSWR(apiRoot + '/locations', fetcher)

  return (
    <div style={{fontFamily: 'Arial, sans-serif', padding: 20}}>
      <h1>Weather Forecast & Alerts — Frontend</h1>
      <p>This simple Next.js frontend fetches the backend API directly.</p>
      <h2>Backend Locations (from API)</h2>
      {apiLocs ? (
        <ul>
          {apiLocs.map(l => <li key={l.id}>{l.name} — {l.lat},{l.lon}</li>)}
        </ul>
      ) : <p>Loading or API unreachable...</p>}
      <hr/>
      <p>Use the Streamlit demo for richer UI (available in /web).</p>
    </div>
  )
}
