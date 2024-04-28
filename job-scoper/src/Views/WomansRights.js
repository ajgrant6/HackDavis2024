import React from 'react';
import '../App.css';

const WomansRights = (props) => {
    const { abortion_policy, employment_discrimination } = props;

    return (
        <div className='FeatureComponent' style={{ textAlign: 'left' }}>
            <h2>Women's Rights</h2>
            <div className='FeatureComponentLine' style={{ lineHeight: '16px'}}>
                <p>{employment_discrimination}</p>
            </div>
            <div className='FeatureComponentLine'>
                <p>Abortion Access:</p>
                <p>{abortion_policy}</p>
            </div>
            <div className='Spacer'/>
        </div>
    );
};

export default WomansRights;