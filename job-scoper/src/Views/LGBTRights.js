import React from 'react';
import '../App.css';
const LGBTRights = (props) => {
    const { ei, ei_legal, ei_po } = props;

    return (
        <div className='FeatureComponent'>
            <h2>LGBTQ+ Equality Index</h2>
            <div className='FeatureComponentLine'>
                <p>Legal:</p>
                <p>{ei_legal}</p>
            </div>
            <div className='FeatureComponentLine'>
                <p>Public Opinion:</p>
                <p>{ei_po}</p>
            </div>
            <div className='FeatureComponentLine'>
                <p>Total:</p>
                <p>{ei}</p>
            </div>
            <div className='Spacer'/>
        </div>
    );
};

export default LGBTRights;