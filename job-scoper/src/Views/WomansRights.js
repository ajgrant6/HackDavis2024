import React from 'react';
import '../App.css';

const WomansRights = (props) => {
    const { abortion_access, lgbt_friendliness } = props;

    return (
        <div className='FeatureComponent'>
            <h2>Rights</h2>
            <div className='FeatureComponentLine'>
                <p>Abortion Access:</p>
                <p>{abortion_access}</p>
            </div>
            <div className='FeatureComponentLine'>
                <p>LGBT Friendliness:</p>
                <p>{lgbt_friendliness}</p>
            </div>
            <div className='Spacer'/>
        </div>
    );
};

export default WomansRights;