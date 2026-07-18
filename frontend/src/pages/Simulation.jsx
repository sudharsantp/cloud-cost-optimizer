import { useState } from "react";
import { simulateEC2 } from "../services/simulationService";

export default function Simulation() {

    const [form, setForm] = useState({
        instance_type: "t3.micro",
        region: "Asia Pacific (Mumbai)",
        quantity: 1,
        hours: 720,
    });

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e) {

        e.preventDefault();

        setLoading(true);

        try {

            const res = await simulateEC2(form);

            setResult(res.data);

        } catch (err) {

            alert("Unable to fetch AWS Pricing.");

        }

        setLoading(false);
    }

    return (

        <div className="p-8">

            <h1 className="text-4xl font-bold mb-8">
                EC2 Cost Simulator
            </h1>

            <form
                onSubmit={handleSubmit}
                className="space-y-5 max-w-xl"
            >

                <select
                    className="w-full border rounded-lg p-3"
                    value={form.instance_type}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            instance_type: e.target.value
                        })
                    }
                >

                    <option>t3.micro</option>
                    <option>t3.small</option>
                    <option>t3.medium</option>
                    <option>t3.large</option>
                    <option>m5.large</option>
                    <option>c5.large</option>
                    <option>g5.xlarge</option>

                </select>

                <select
                    className="w-full border rounded-lg p-3"
                    value={form.region}
                    onChange={(e) =>
                        setForm({
                            ...form,
                            region: e.target.value
                        })
                    }
                >

                    <option>Asia Pacific (Mumbai)</option>
                    <option>US East (N. Virginia)</option>
                    <option>EU (Ireland)</option>

                </select>

                <input
                    type="number"
                    className="w-full border rounded-lg p-3"
                    placeholder="Quantity"
                    value={form.quantity}
                    min="1"
                    onChange={(e) =>
                        setForm({
                            ...form,
                            quantity: Number(e.target.value)
                        })
                    }
                />

                <input
                    type="number"
                    className="w-full border rounded-lg p-3"
                    placeholder="Hours"
                    value={form.hours}
                    min="1"
                    onChange={(e) =>
                        setForm({
                            ...form,
                            hours: Number(e.target.value)
                        })
                    }
                />

                <button
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg disabled:bg-gray-400"
                >
                    {loading ? "Calculating..." : "Simulate"}
                </button>

            </form>

            {result && (

                <>

                    <div className="grid grid-cols-2 gap-6 mt-10">

                        <div className="bg-white rounded-xl shadow p-6">

                            <p className="text-gray-500">
                                Hourly Price
                            </p>

                            <h2 className="text-3xl font-bold text-blue-600 mt-2">

                                ${Number(result.hourly_price).toFixed(4)}

                            </h2>

                        </div>

                        <div className="bg-white rounded-xl shadow p-6">

                            <p className="text-gray-500">
                                Estimated Cost
                            </p>

                            <h2 className="text-3xl font-bold text-green-600 mt-2">

                                ${Number(result.estimated_cost).toFixed(2)}

                            </h2>

                        </div>

                    </div>

                    <div className="grid grid-cols-2 gap-6 mt-6">

                        <div className="bg-white rounded-xl shadow p-6">

                            <p className="text-gray-500">
                                Estimated Daily Cost
                            </p>

                            <h2 className="text-3xl font-bold mt-2">

                                $

                                {(
                                    Number(result.estimated_cost) /
                                    (form.hours / 24)
                                ).toFixed(2)}

                            </h2>

                        </div>

                        <div className="bg-white rounded-xl shadow p-6">

                            <p className="text-gray-500">
                                Currency
                            </p>

                            <h2 className="text-3xl font-bold mt-2">

                                {result.currency}

                            </h2>

                        </div>

                    </div>

                </>

            )}

        </div>

    );

}