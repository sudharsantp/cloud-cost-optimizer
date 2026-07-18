import useFetch from "../hooks/useFetch";

import {
    getDailyCost,
    getServiceBreakdown
} from "../services/analyticsService";

import DailyCostChart from "../charts/DailyCostChart";
import ServicePieChart from "../charts/ServicePieChart";

export default function Analytics() {

    const daily = useFetch(getDailyCost);

    const services = useFetch(getServiceBreakdown);

    if (daily.loading || services.loading)
        return <h2>Loading...</h2>;

    if (daily.error)
        return <h2>{daily.error}</h2>;

    if (services.error)
        return <h2>{services.error}</h2>;

    return (

        <div className="space-y-6">

            <h1 className="text-3xl font-bold">
                Analytics
            </h1>

            <div className="grid lg:grid-cols-2 gap-6">

                <DailyCostChart
                    data={daily.data}
                />

                <ServicePieChart
                    data={services.data}
                />

            </div>

        </div>

    );

}