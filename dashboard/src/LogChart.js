import React, {useState, useEffect} from "react";
import {Chart, CategoryScale} from "chart.js/auto"
import {Line} from "react-chartjs-2"

Chart.register(CategoryScale);
const LogChart = ({endpoint}) => {

    const [data, setData] = useState({});
    const [loading, setLoading] = useState(true); // Add a loading state

    useEffect(() => {
        // fetch logging data from the API
        fetch(endpoint)
            .then(response => response.json())
            .then(logData => {
                // update the component's state with the received data
                setData({
                    labels: logData.map(item => item.timestamp),
                    datasets: [
                        {
                            label: "Response Time (s)",
                            yAxisID: "response_time",
                            data: logData.map(item => item.response_time),
                            type: "line",
                            borderColor: "rgba(104, 220, 251, 0.8)",
                            borderWidth: 5,
                        },
                        {
                            label: "Status Code",
                            yAxisID: "status_code",
                            data: logData.map(item => item.status_code),
                            type: "bar",
                            backgroundColor: (context) => {
                                const index = context.dataIndex;
                                const value = context.dataset.data[index];
                                return value == 200 ? "rgba(162, 255, 167, 0.51)" : "rgba(251, 104, 104, 0.51)";
                            }
                        }
                    ],
                    options: {
                        scales: {
                            yAxes: [{
                                id: "response_time",
                                type: "linear",
                                position: "left",
                                ticks: {
                                    beginAtZero: true,
                                    max: 0.1,
                                }
                            }, {
                                id: "status_code",
                                type: "linear",
                                position: "right",
                                ticks: {
                                    beginAtZero: true,
                                }
                            }
                            ],
                            x: {
                                type: "time",
                            },
                            y: {
                                beginAtZero: true,
                            }
                        },
                    }
                });
                setLoading(false); // set loading to false when the data is received
            })
            .catch(error => console.error(error));
    }, [endpoint]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return <Line data={data}/>;
};

export default LogChart;
