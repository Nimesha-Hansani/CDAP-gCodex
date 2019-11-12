import React, { Component } from 'react';
import {
    Navbar,Container,NavbarBrand,NavLink,NavItem,Nav,
    Button,Row,Col
    
  } from 'reactstrap';


export default class Dashboard extends Component {
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
                   <img src="https://cdn3.iconfinder.com/data/icons/users-23/64/_Male_Profile_Round_Circle_Users-512.png" alt="Avatar" class="avatar"/>
                </NavItem>
                <NavItem style={{marginTop:'8px'}}>
                        <Button color="secondary" href="/">Sign Out</Button>{' '}
                </NavItem>
                </Nav>
            </Container>
            </Navbar>
            
            <Row>
                <Col lg ={2} id="btnCol" >
                <Row id ="btn">
                <Button id="DB"outline color="info">Repo Structure</Button>
                <Button id="DB"outline color="info">Complexity</Button>
                <Button id="DB"outline color="info">Cognitvity</Button>
                <Button id="DB"outline color="info">Bugs</Button>
                <Button id="DB"outline color="info">Other</Button>
                </Row>
                </Col>
                <Col lg ={10}>

                </Col>
            </Row>

            </div>
        )
    }
}
