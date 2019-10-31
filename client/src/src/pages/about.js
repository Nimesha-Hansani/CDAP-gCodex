import React, { Component } from 'react';
import {
    Navbar,
    NavbarBrand, Nav,NavItem,NavLink, Container
  } from 'reactstrap';
  

export default class about extends Component {
    render() {
        return (
            <div>
              <Navbar class="navBackground" color="info" light expand="md">
            <Container>
                <NavbarBrand id="navBrand" href="/">About</NavbarBrand>
                <Nav className="ml-auto" navbar>
                <NavItem>
                    <NavLink id="sample" href="/">Home</NavLink>
                </NavItem>
                </Nav>
            </Container>
         </Navbar>

                
            </div>
        )
    }
}
