import { NavLink } from "react-router-dom";

const links = [
  { name: "Dashboard", path: "/" },
  { name: "Analytics", path: "/analytics" },
  { name: "Forecast", path: "/forecast" },
  { name: "Recommendations", path: "/recommendations" },
  { name: "Simulation", path: "/simulation" },
  { name: "Cost Health", path: "/health" },
  { name: "Settings", path: "/settings" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col min-h-screen">
      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <h2 className="text-xl font-bold leading-8">
          CloudWatch Billing
          <br />
          Sentinel
        </h2>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">

        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            end={link.path === "/"}
            className={({ isActive }) =>
              `block px-4 py-3 rounded-lg mb-2 transition-all duration-200 font-medium ${isActive
                ? "bg-blue-600 text-white shadow-lg"
                : "text-slate-200 hover:bg-slate-800 hover:text-white"
              }`
            }
          >
            {link.name}
          </NavLink>
        ))}

      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-700 text-xs text-slate-400 text-center">
        CloudWatch Billing Sentinel
        <br />
        Version 1.0
      </div>

    </aside>
  );
}