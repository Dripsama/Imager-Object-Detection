import React from 'react'
import './About.css';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import TimelapseIcon from '@material-ui/icons/Timelapse';
import VerifiedUserRoundedIcon from '@material-ui/icons/VerifiedUserRounded';

export default function About() {
    return (
        <div className="row">
            <div className="feature-box">
                <CheckCircleIcon style={{color: "white", fontSize: "3rem"}}/>
                <h3 className="feature-title">Easy to use</h3>
                <p  className="content">Just have to Upload or Drag and Drop an Image</p>
            </div>
            <div className="feature-box">
                <TimelapseIcon style={{color: "white", fontSize: "3rem"}}/>
                <h3 className="feature-title">Quick and Responsive</h3>
                <p className="content">Results Displayed within Seconds</p>
            </div>
            <div className="feature-box">
                <VerifiedUserRoundedIcon style={{color: "white", fontSize: "3rem"}}/>
                <h3 className="feature-title">Guaranteed to Work</h3>
                <p className="content">High Accuracy in getting Necessary Results</p>
            </div> 
        </div>
    )
}
