export default function Navbar() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">

      <h1 className="text-xl font-semibold text-slate-700">
        AWS Cost Intelligence
      </h1>

      <button
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
      >
        Sync AWS
      </button>

    </header>
  );
}