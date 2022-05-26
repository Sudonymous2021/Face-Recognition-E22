import React from 'react';
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import { Nav, Navbar, Container } from 'react-bootstrap';

export default function NavbarComp() {
  return (
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Container>
          <Navbar.Brand as={Link} to={"/"}>Smartify-Attendance</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="me-auto">
              {/* <Nav.Link as={Link} to={"/Register"}>Register Student</Nav.Link> */}
              {/* <Nav.Link as={Link} to={"/ClassList"}>Class List</Nav.Link> */}
              <Nav.Link as={Link} to={"/TakeAttendance"}>Take Attendance</Nav.Link>
              {/* <Nav.Link as={Link} to={"/ViewAttendance"}>View Attendance</Nav.Link> */}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>   
  )
}
