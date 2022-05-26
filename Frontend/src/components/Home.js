import React, { Component } from 'react'
import './Image.css'

export default class Home extends Component {
  render() {
    return (
      <>
      <div>
        <img src='webcam'id='MainImage' alt='Server is not running'></img>
      </div>
      <div className='download'>
        <a href='http://localhost:5000/download'><button variant="danger">Download Attendance</button></a>
      </div>
      </>
    )
  }
}

