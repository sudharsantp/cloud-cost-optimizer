import useFetch from "../hooks/useFetch";
import { getForecastSummary } from "../services/forecastService";

export default function Dashboard() {
    const { data, loading, error } = useFetch(getForecastSummary);

    if (loading) {
        return (
            <h2 className="text-xl font-semibold">
                Loading...
            </h2>
        );
    }

    if (error) {
        return (
            <h2 className="text-red-600 font-semibold">
                {error}
            </h2>
        );
    }

    return (
        <div className="space-y-6">

            <h2 className="text-3xl font-bold">
                Dashboard
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

                <div className="bg-white rounded-xl shadow p-6">
                    <p className="text-slate-500">
                        Tomorrow Prediction
                    </p>

                    <h2 className="text-3xl font-bold mt-2">
                        ${data.tomorrow_prediction}
                    </h2>
                </div>

                <div className="bg-white rounded-xl shadow p-6">
                    <p className="text-slate-500">
                        Next 7 Days
                    </p>

                    <h2 className="text-3xl font-bold mt-2">
                        ${data.next_7_days_total}
                    </h2>
                </div>

                <div className="bg-white rounded-xl shadow p-6">
                    <p className="text-slate-500">
                        Next 30 Days
                    </p>

                    <h2 className="text-3xl font-bold mt-2">
                        ${data.next_30_days_total}
                    </h2>
                </div>

                <div className="bg-white rounded-xl shadow p-6">
                    <p className="text-slate-500">
                        Highest Predicted Cost
                    </p>

                    <h2 className="text-3xl font-bold mt-2">
                        ${data.highest_cost}
                    </h2>

                    <p className="text-sm text-slate-500 mt-3">
                        {data.highest_predicted_day}
                    </p>
                </div>

            </div>

        </div>
    );
}