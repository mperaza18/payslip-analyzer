import HealthBadge from './HealthBadge'

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between border-b border-gray-700 bg-gray-900 px-6 py-3">
      <span className="text-lg font-semibold text-white">Payslip Analyzer</span>
      <HealthBadge />
    </nav>
  )
}
