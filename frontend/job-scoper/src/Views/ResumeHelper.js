import React, { useState, useEffect } from 'react';
import '../App.css';
import axios from 'axios';

const ResumeHelper = (props) => {
    const [pdfAsText, setPdfAsText] = useState('');
    const [jobDescription, setJobDescription] = useState('');
    const [comparisonResult, setComparisonResult] = useState('');
    const [loading, setLoading] = useState(false); // Add loading state

    useEffect(() => {
        fetchJobDescription(props.jobLink);
    }, [props.jobLink]);

    const fetchJobDescription = async (link) => {
        try {
            const response = await axios.post('http://localhost:8080/api/getJobDescription', { link });
            if (response.data.job_description) {
                setJobDescription(response.data.job_description);
            } else {
                console.error('Job description not found:', response.data.error);
            }
        } catch (error) {
            console.error('Error fetching job description:', error);
        }
    };

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8080/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.data.text) {
                setPdfAsText(response.data.text);
            } else {
                console.error('Failed to extract text:', response.data.error);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    const compareResumes = async () => {
        setLoading(true); // Set loading to true when the button is clicked
        try {
            const response = await axios.post('http://localhost:8080/api/compareResume', {
                resume_text: pdfAsText,
                job_description: jobDescription
            });

            if (response.data) {
                setComparisonResult(response.data);
            } else {
                console.error('Comparison failed:', response.data.error);
            }
        } catch (error) {
            console.error('Error comparing resumes:', error);
        } finally {
            setLoading(false); // Set loading back to false after comparison
        }
    };

    return (
        <div className="ResumeHelper" style={{ margin: "0 auto", textAlign: "center" }}>
            <div className='ResumeHelperHeading'>
                <h1>Resume Helper</h1>
                <p>Let's see if you're a good fit!</p>
                <p className='Italics'>Powered by OpenAI</p>
            </div>
            <div className="ResumeUpload">
                <h2>Upload Resume</h2>
                <input type="file" id="resume" name="resume" accept=".pdf" onChange={handleFileUpload}  />
                
            </div>
            <div className="ResumeHelperArea">
                <div style={{ flexDirection: 'row' }}>
                    <div className="ResumeComponent">
                        <div className="JobDescription">
                            <h2 style={{ textAlign: "center" }}>AI Analysis</h2>
                            <div style={{ textAlign: "center", marginBottom: "20px" }}>
                                <button onClick={compareResumes} style={{borderRadius: '5px', fontSize: '18px', padding: '2px 5px'}}>Generate Analysis</button>
                            </div>
                            <div className='JobDescriptionText' style={{ padding: "10px", fontSize: "1.2em" }}>
                                {loading ? (
                                    <div style={{ display: "flex", justifyContent: "center" }}>
                                        <img src={require('../loading.gif')} alt="Loading..." style={{ width: "75%", margin: "0 auto" }} />
                                    </div>
                                ) : (
                                    <div dangerouslySetInnerHTML={{ __html: comparisonResult || "Upload your resume and click 'Generate Analysis' to see how you match up!" }} />
                                )}
                            </div>
                            <div className="Spacer"/>
                        </div>
                    </div>
                    <div className="Spacer"/>
                    <div className='JobDescription'>
                        <h2 style={{ textAlign: "center" }}>Job Description</h2>
                        {jobDescription ? (
                            <p className='JobDescriptionText' style={{ fontSize: "1.2em" }}>{jobDescription}</p>
                        ) : (
                            <div style={{ display: "flex", justifyContent: "center" }}>
                                <img src={require('../loading.gif')} alt="Loading..." style={{ width: "50%", margin: "0 auto" }} />
                            </div>
                        )}
                        <div className="Spacer"/>
                    </div>
                    <div className="Spacer"/>
                </div>
            </div>
        </div>
    );
}

export default ResumeHelper;
