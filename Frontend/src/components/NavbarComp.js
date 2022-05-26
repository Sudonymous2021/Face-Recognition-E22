import React from 'react';
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import { Nav, Navbar, Container } from 'react-bootstrap';

export default function NavbarComp() {
  return (
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Container>
          <Navbar.Brand as={Link} to={"/"}>Smart-Attendance</Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Nav.Link>Made By Srivatsa Sudhamsh Chakravartula</Nav.Link>
        </Container>
      </Navbar>   
  )
}
