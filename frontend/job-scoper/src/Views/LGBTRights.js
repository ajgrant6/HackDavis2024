import React, { useState, useEffect } from 'react';
import '../App.css';

const LGBTRights = (props) => {
    const { state_id } = props;
    const [equaldexURL, setEqualdexURL] = useState(null);

    useEffect(() => {
        if (state_id) {
            setEqualdexURL(`https://www.equaldex.com/embed/topic?region=US-${state_id}&color=616161`);
        } else {
            setEqualdexURL(null);
        }
    }, [state_id]); // Re-run this effect whenever state_id changes

    return (
        <div className='FeatureComponent' style={{ textAlign: 'left' }}>
            <h2>LGBTQ+ Rights 🏳️‍🌈</h2>
            {/* <div className='FeatureComponentLine' style={{ marginBottom: '15px', marginTop: '15px' }}>
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

            <hr className='MoreDetails'/>
            <br /><br /><br />


            <div className='FeatureComponentLine' style={{ marginBottom: '15px' }}>
                <p className='ZeroPaddingMargin'>Gender Affirming Care:</p>
                <p className='ZeroPaddingMargin'>{genderafirm_legality}</p>
            </div>

            <hr className='MoreDetails'/>
            <br /><br /><br />

            <div className='FeatureComponentLine' >
            <p className='ZeroPaddingMargin'>{employment_discrimination}</p>
            </div>

            <div className='Spacer'/> */}
            {state_id ? (
                <iframe
                    src={equaldexURL}
                    width="100%"
                    height="400"
                    style={{
                        border: 'none',
                        borderRadius: '10px',
                        // boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                        marginTop: '20px'
                        // backgroundColor: 'rgba(71, 163, 255, 0.8)',
                    }}
                    title="Equaldex LGBT Rights Overview"
                    sandbox="allow-same-origin allow-scripts"
                ></iframe>
            ) : (
                <p>No Data</p>
            )}
        <div className='Spacer'/>
        </div>
    );
};

export default LGBTRights;
