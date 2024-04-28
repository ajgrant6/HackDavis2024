import React from 'react';
import '../App.css';

const LGBTRights = (props) => {
    const { ei, ei_legal, ei_po, genderafirm_legality, employment_discrimination } = props;

    return (
        <div className='FeatureComponent'>
            <h2>LGBTQ+ Rights</h2>
            <div className='FeatureComponentLine'>
                <p>Equality Index:</p>
                <p>{ei}</p>
            </div>
            <div className='MoreDetails'>
                <div className='FeatureComponentLine'>
                    <p>Legal Equality Index:</p>
                    <p>{ei_legal}</p>
                </div>
                <div className='FeatureComponentLine'>
                    <p>Public Opinion Index:</p>
                    <p>{ei_po}</p>
                </div>
                <div className='FeatureComponentLine'>
                    <p>Gender Affirmative Care:</p>
                    <p>{genderafirm_legality}</p>
                </div>
                <div>
                    <p>{employment_discrimination}</p>
                </div>
            </div>
            <div className='Spacer'/>
        </div>
    );
};

export default LGBTRights;
