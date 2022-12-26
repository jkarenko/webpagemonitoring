import "./App.css";
import LogChart from "./LogChart";
import React from "react";

const API_URL = "http://127.0.0.1:8000/"

function App() {
    // fetch list of monitored endpoints
    const [endpoints, setEndpoints] = React.useState([]);
    React.useEffect(() => {
        fetch(API_URL)
            .then(response => response.json())
            .then(data => setEndpoints(data))
            .catch(error => console.error(error));
    }, []);

    return (
        <div className="App">
            <div className="App-header">
                <h1>Dashboard</h1>
            </div>
            <div className="Charts-container">
                {endpoints.map(endpoint => (
                    <div className="Chart-item" key={endpoint.name}>
                        <h2>{endpoint.name}</h2>
                        <LogChart endpoint={API_URL + "log/" + endpoint.name}/>
                    </div>
                ))}
            </div>
        </div>

    );
}

export default App;
