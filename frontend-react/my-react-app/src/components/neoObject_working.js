import axios from 'axios';
import React, { useEffect, useState } from 'react';
import '../static/neoObjectApproach.css';

const NeoObject = ({ selectedObject }) => {
    const [approachData, setApproachData] = useState(null);
    const [orbitData, setOrbitData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [identifier, setIdentifier] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            if (selectedObject) {
                setLoading(true);
                setApproachData(null);
                setOrbitData(null)
                setIdentifier(null);
                try {
                    const response = await axios.post('http://127.0.0.1:5000/api/neoObject', selectedObject);
                    const dataArray = JSON.parse(response.data.data)
                    setApproachData(dataArray.sorted_approaches);
                    setOrbitData(dataArray.orbital_data)
                    setMessage(response.data.message);
                    setIdentifier(response.data.identifier)
                    
                } catch (error) {
                    setMessage('Error occurred');
                }
                setLoading(false);
            }
        };
        fetchData();
    }, [selectedObject]); // Fetch data whenever selectedObject changes

    // every time data is updated
    useEffect(() => {
        if (approachData) {
        console.log(approachData)
        console.log(orbitData)

        }
    }, [approachData]); // This triggers when 'data' changes
    
    if (approachData && Array.isArray(approachData)) {
        return (
            <div id="user-obj-data-wrapper">
                {loading && <p>Loading...</p>}                

                <div className="obj-orbit-data-container">
                    {orbitData.map((item, index) => (
                        <div key={index} className="obj-orbit-data">
                            <p><strong>Orbit ID:</strong> {item.orbit_id}</p>
                            <p><strong>Orbit Determination Date:</strong> {item.orbit_determination_date}</p>
                            <p><strong>First Observation Date:</strong> {item.first_observation_date}</p>
                            <p><strong>Last Observation Date:</strong> {item.last_observation_date}</p>
                            <p><strong>Data Arc (in Days):</strong> {item.data_arc_in_days}</p>
                            <p><strong>Observations Used:</strong> {item.observations_used}</p>
                            <p><strong>Orbit Uncertainty:</strong> {item.orbit_uncertainty}</p>
                            <p><strong>Minimum Orbit Intersection:</strong> {item.minimum_orbit_intersection}</p>
                            <p><strong>Jupiter Tisserand Invariant:</strong> {item.jupiter_tisserand_invariant}</p>
                            <p><strong>Epoch Osculation:</strong> {item.epoch_osculation}</p>
                            <p><strong>Eccentricity:</strong> {item.eccentricity}</p>
                            <p><strong>Semi-Major Axis:</strong> {item.semi_major_axis}</p>
                            <p><strong>Inclination:</strong> {item.inclination}</p>
                            <p><strong>Ascending Node Longitude:</strong> {item.ascending_node_longitude}</p>
                            <p><strong>Orbital Period:</strong> {item.orbital_period}</p>
                            <p><strong>Perihelion Distance:</strong> {item.perihelion_distance}</p>
                            <p><strong>Perihelion Argument:</strong> {item.perihelion_argument}</p>
                            <p><strong>Aphelion Distance:</strong> {item.aphelion_distance}</p>
                            <p><strong>Perihelion Time:</strong> {item.perihelion_time}</p>
                            <p><strong>Mean Anomaly:</strong> {item.mean_anomaly}</p>
                            <p><strong>Mean Motion:</strong> {item.mean_motion}</p>
                            <p><strong>Equinox:</strong> {item.equinox}</p>
                            {/* <p><strong>Orbit Class Type:</strong> {item.orbit_class.orbit_class_type}</p>
                            <p><strong>Orbit Class Description:</strong> {item.orbit_class.orbit_class_description}</p>
                            <p><strong>Orbit Class Range:</strong> {item.orbit_class.orbit_class_range}</p> */}
                        </div>
                    ))}
                </div>
                <div className="user-approach-data-container">
                    {approachData.map((item, index) => (
                        <div key={index} className="user-approach-data">
                            <p><strong>Close Approach Date:</strong> {item.close_approach_date}</p>
                            <p><strong>Full Date:</strong> {item.close_approach_date_full}</p>
                            <p><strong>Miss Distance (Astronomical):</strong> {item.miss_distance.astronomical}</p>
                            <p><strong>Miss Distance (Kilometers):</strong> {item.miss_distance.kilometers}</p>
                            <p><strong>Miss Distance (Lunar):</strong> {item.miss_distance.lunar}</p>
                            <p><strong>Miss Distance (Miles):</strong> {item.miss_distance.miles}</p>
                            <p><strong>Orbiting Body:</strong> {item.orbiting_body}</p>
                            <p><strong>Relative Velocity (km/h):</strong> {item.relative_velocity.kilometers_per_hour}</p>
                            <p><strong>Relative Velocity (km/s):</strong> {item.relative_velocity.kilometers_per_second}</p>
                            <p><strong>Relative Velocity (miles/h):</strong> {item.relative_velocity.miles_per_hour}</p>
                        </div>
                    ))}
                </div>
            </div>    
            
        );
    } else {
        return 
    }
    
};

export default NeoObject;
