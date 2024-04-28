import React from 'react';
import '../App.css';
const WalkAbility = (props) => {
    const { walkScore, transitScore, bikeScore } = props;

    return (
        <div className='FeatureComponent'>
            <h2>Commuting</h2>
            <div className='FeatureComponentLine'>
                <p>Walk-Score:</p>
                <p>{walkScore}</p>
            </div>
            <div className='FeatureComponentLine'>
                <p>Transit-Score:</p>
                <p>{transitScore}</p>
            </div>
            <div className='FeatureComponentLine'>
                <p>Bike-Score:</p>
                <p>{bikeScore}</p>
            </div>
            <div className='Spacer'/>
        </div>
    );
};

export default WalkAbility;