import { NavLink } from "react-router-dom";

const links = [
  { name: "Dashboard", path: "/" },
  { name: "Analytics", path: "/analytics" },
  { name: "Forecast", path: "/forecast" },
  { name: "Recommendations", path: "/recommendations" },
  { name: "Settings", path: "/settings" },
  { name: "Simulation", path: "/simulation" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col">

      <div className="p-6 border-b border-slate-700">
        <h2 className="text-xl font-bold">
          CloudWatch Billing Sentinel
        </h2>
      </div>

      <nav className="flex-1 p-4">

        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            end={link.path === "/"}
            className={({ isActive }) =>
              `block px-4 py-3 rounded-lg mb-2 ${isActive
                ? "bg-blue-600"
                : "hover:bg-slate-800"
              }`
            }
          >
            {link.name}
          </NavLink>
        ))}

      </nav>

    </aside>
  );
}