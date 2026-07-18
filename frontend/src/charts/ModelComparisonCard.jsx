export default function ModelComparisonCard({ comparison }) {

    return (

        <div className="grid grid-cols-3 gap-6">

            <div className="bg-white rounded-xl shadow p-6">

                <h2 className="text-xl font-semibold mb-4">
                    Facebook Prophet
                </h2>

                <p>MAE : {comparison.Prophet.MAE}</p>

                <p>RMSE : {comparison.Prophet.RMSE}</p>

            </div>

            <div className="bg-white rounded-xl shadow p-6">

                <h2 className="text-xl font-semibold mb-4">
                    ARIMA
                </h2>

                <p>MAE : {comparison.ARIMA.MAE}</p>

                <p>RMSE : {comparison.ARIMA.RMSE}</p>

            </div>

            <div className="bg-green-600 text-white rounded-xl shadow p-6">

                <h2 className="text-xl font-semibold">
                    Best Model
                </h2>

                <p className="text-3xl mt-6 font-bold">
                    {comparison.Best_Model}
                </p>

            </div>

        </div>

    );

}