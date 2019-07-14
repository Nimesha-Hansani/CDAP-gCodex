import React, { Component } from 'react';
import {
    Navbar,Container,NavbarBrand,NavLink,NavItem,Nav

    
  } from 'reactstrap';

export default class UserMenu extends Component {
    render() {
        return (
            <div>
            <Navbar class="navBackground" color="info" light expand="md">
            <Container>
                <NavbarBrand id="navToolName" href="/">gCodex</NavbarBrand>
                <Nav className="ml-auto" navbar>
         
                <NavItem>
                    <NavLink id="sample" href="/about">About</NavLink>
                </NavItem>
                <NavItem>
                    <NavLink id="sample" href="/about">Nimesha -Hansani</NavLink>
                </NavItem>
                <NavItem>
                    
                </NavItem>
                </Nav>
            </Container>
            </Navbar>
                
            </div>
        )
    }
}
