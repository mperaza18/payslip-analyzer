import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Navbar />
      <Dashboard />
    </div>
  )
}
