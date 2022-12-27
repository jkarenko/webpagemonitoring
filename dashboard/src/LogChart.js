import React, {useState, useEffect} from "react";
import {Chart, CategoryScale} from "chart.js/auto"
import {Line} from "react-chartjs-2"

Chart.register(CategoryScale);
const LogChart = ({endpoint}) => {

    const [data, setData] = useState({});
    const [loading, setLoading] = useState(true); // Add a loading state
    const fetchLog = () => {
        // fetch logging data from the API
        fetch(endpoint)
            .then(response => response.json())
            .then(logData => {
                // update the component's state with the received data
                setData({
                    id: logData.title,
                    labels: logData.map(item => item.timestamp),
                    title: logData[0].url,
                    datasets: [
                        {
                            label: "Response Time (s)",
                            yAxisID: "response_time",
                            data: logData.map(item => item.response_time),
                            type: "line",
                            borderColor: "rgba(104, 220, 251, 0.8)",
                            borderWidth: 10,
                            tension: 0.2,
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
                });
                setLoading(false); // set loading to false when the data is received
            })
            .catch(error => console.error(error));
    }

    // fetch the data when the component mounts
    useEffect(() => {
        fetchLog();
        // fetch the data every 10 seconds
        setInterval(() => {
            fetchLog();
        }, 30000);

    }, [endpoint]);

    if (loading) {
        return <div>Loading...</div>;
    }
    const options = {
        // responsive: true,
        plugins: {
            legend: {
                position: 'top',
                display: false,
            },
            title: {
                display: true,
                text: data.title,
                font: {
                    size: 20,
                }
            },
        },
        // scales: {
        //     y1: {
        //         type: "linear",
        //         display: true,
        //         position: "right",
        //         id: "response_time",
        //         title: {
        //             display: true,
        //             text: "Response Time (s)",
        //         },
        //         ticks: {
        //             beginAtZero: true,
        //             max: 10,
        //         }
        //     },
        //     y2: {
        //         type: "linear",
        //         display: true,
        //         position: "left",
        //         id: "status_code",
        //         title: {
        //             display: true,
        //             text: "Status Code",
        //         }
        //     }
        //
        // }
    }

    return <Line options={options} data={data}/>;
};

export default LogChart;
