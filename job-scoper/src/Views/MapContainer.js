import React from 'react';
import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';



const MapContainer = (props) => {
    const mapStyles = {
        width: '50%',
        height: '500px',
        margin: '0 auto',
        borderRadius: '10px'
    };
  
    const { latIn, lonIn } = props;
  
    return (

        <Map
            google={props.google}
            zoom={14}
          style={mapStyles}
          initialCenter={{
            lat: latIn,
            lng: lonIn
            }}
          containerStyle={{ height: '500px' }}
        >
            <Marker position={{ lat: parseInt(latIn), lng: parseInt(lonIn) }} />
        </Map>

    );
  };

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLEAPI
})(MapContainer);