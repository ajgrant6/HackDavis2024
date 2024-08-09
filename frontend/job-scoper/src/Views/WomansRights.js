import React from 'react';
import '../App.css';

const WomansRights = (props) => {
    const { abortion_policy, employment_discrimination } = props;

    return (
        <div className='FeatureComponent' style={{ textAlign: 'left' }}>
            <h2>Women's Rights 💁🏻‍♀️</h2>
            <div className='FeatureComponentLine' style={{ marginBottom: '0px' }}>
                <p >{employment_discrimination}</p>
            </div>

            <hr className='MoreDetails'/>
            <br /><br /><br />


            <div className='FeatureComponentLine'  style={{ marginTop: '0px' }}>
                <p className='ZeroPaddingMargin'>Abortion Access:</p>
                <p className='ZeroPaddingMargin'>{abortion_policy}</p>
            </div>
            <div className='Spacer'/>
        </div>
    );
};

export default WomansRights;