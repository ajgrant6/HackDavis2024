import React from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const MapContainer = (props) => {
    const mapStyles = {
        width: '50%',
        height: '500px',
        margin: '0 auto',
        borderRadius: '10px'
    };

    const { latIn, lonIn } = props;

    const center = {
        lat: parseFloat(latIn),
        lng: parseFloat(lonIn)
    };

    return (
        <LoadScript googleMapsApiKey={process.env.REACT_APP_GOOGLEAPI}>
            <GoogleMap
                mapContainerStyle={mapStyles}
                center={center}
                zoom={14}
            >
                <Marker position={center} />
            </GoogleMap>
        </LoadScript>
    );
};

export default MapContainer;