import React from "react";
import howtoimg from "../assets/images/How_To.png";
import "../App.css";

const HowTo = () => {
    return (
        <div className="howto-container">
            <img src={howtoimg} alt="How to use Job Scoper" className="howto-image"/>
        </div>
    );
};

export default HowTo;