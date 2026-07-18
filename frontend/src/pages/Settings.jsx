import { useState } from "react";
import useFetch from "../hooks/useFetch";
import {
    getBackendStatus,
    syncAWS,
} from "../services/settingsService";

export default function Settings() {

    const { data, loading, error, refetch } =
        useFetch(getBackendStatus);

    const [syncing, setSyncing] = useState(false);

    async function handleSync() {

        setSyncing(true);

        try {

            await syncAWS();

            alert("AWS Billing synchronized successfully.");

            refetch();

        } catch {

            alert("Synchronization failed.");

        }

        setSyncing(false);

    }

    if (loading)
        return <h2>Loading...</h2>;

    if (error)
        return <h2>{error}</h2>;

    return (

        <div className="space-y-6">

            <h1 className="text-3xl font-bold">
                Settings
            </h1>

            <div className="bg-white rounded-xl shadow p-6">

                <h2 className="text-xl font-semibold mb-5">
                    Backend Status
                </h2>

                <p>
                    <b>Project :</b> {data.project}
                </p>

                <p>
                    <b>Version :</b> {data.version}
                </p>

                <p>
                    <b>Status :</b>

                    <span className="text-green-600 font-semibold">
                        {" "}
                        {data.status}
                    </span>

                </p>

            </div>

            <div className="bg-white rounded-xl shadow p-6">

                <h2 className="text-xl font-semibold mb-5">
                    AWS Synchronization
                </h2>

                <button
                    onClick={handleSync}
                    disabled={syncing}
                    className="bg-blue-600 text-white px-5 py-3 rounded-lg hover:bg-blue-700"
                >

                    {syncing
                        ? "Synchronizing..."
                        : "Sync AWS Billing"}

                </button>

            </div>

        </div>

    );

}