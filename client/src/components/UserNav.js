import React from 'react';
import {
    Navbar,
    NavbarBrand, Nav,NavItem,NavLink,Container,Button, 
  } from 'reactstrap';


export default function UserNav() {
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
                    <NavLink id="sample" href="/about">Nimesansani</NavLink>
                </NavItem>
                <NavItem>
                   <img src="https://cdn3.iconfinder.com/data/icons/users-23/64/_Male_Profile_Round_Circle_Users-512.png" alt="Avatar" class="avatar"/>
                </NavItem>
                <NavItem style={{marginTop:'8px'}}>
                        <Button color="secondary" href="/">Sign Out</Button>{' '}
                </NavItem>
                </Nav>
            </Container>
            </Navbar>
            
        </div>
    )
}
