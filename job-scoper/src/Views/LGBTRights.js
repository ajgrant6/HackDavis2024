import React from 'react';
import '../App.css';

const LGBTRights = (props) => {
    const { ei, ei_legal, ei_po, genderafirm_legality, employment_discrimination } = props;

    return (
        <div className='FeatureComponent' style={{ textAlign: 'left' }}>
            <h2>LGBTQ+ Rights</h2>
            <div className='FeatureComponentLine' style={{ marginBottom: '15px', marginTop: '15px' }}>
                <p className='ZeroPaddingMargin'>Equality Index:</p>
                <p className='ZeroPaddingMargin'>{ei}</p>
            </div>

                <div className='FeatureComponentLine' style={{ marginBottom: '15px' }}>
                    <p className='ZeroPaddingMargin'>Legal Equality Index:</p>
                    <p className='ZeroPaddingMargin'>{ei_legal}</p>
                </div>
                <div className='FeatureComponentLine' style={{ marginBottom: '15px' }}>
                    <p className='ZeroPaddingMargin'>Public Opinion Index:</p>
                    <p className='ZeroPaddingMargin'>{ei_po}</p>
                </div>
                <div className='FeatureComponentLine' style={{ marginBottom: '15px' }}>
                    <p className='ZeroPaddingMargin'>Gender Affirming Care:</p>
                    <p className='ZeroPaddingMargin'>{genderafirm_legality}</p>
                </div>
                <div className='FeatureComponentLine' >
                <p className='ZeroPaddingMargin'>{employment_discrimination}</p>
                </div>

            <div className='Spacer'/>
        </div>
    );
};

export default LGBTRights;
