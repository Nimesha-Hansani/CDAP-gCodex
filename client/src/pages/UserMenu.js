import React, { Component } from 'react';
import {
    Navbar,Container,NavbarBrand,NavLink,NavItem,Nav,Row,
    Col,Button,Form,FormGroup,Input,
    Label

    
  } from 'reactstrap';
  // import UserNav from '../components/UserNav';

export default class UserMenu extends Component {

  constructor(props){
    super(props);
    this.state = {
        
    };
    
}


    render() {
        return (
            <div>
            <Navbar className="navBackground" color="info" light expand="md">
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
                   <img src="https://cdn3.iconfinder.com/data/icons/users-23/64/_Male_Profile_Round_Circle_Users-512.png" alt="Avatar" className="avatar"/>
                </NavItem>
                <NavItem style={{marginTop:'8px'}}>
                        <Button color="secondary" href="/">Sign Out</Button>{' '}
                </NavItem>
                </Nav>
            </Container>
            </Navbar>


            {/* <UserNav/> */}

            <Row>
            <Col lg={5} id="A1"style={{paddingLeft:'30px',paddingTop:'20px'}}>
            <h3 className="SearchText">Search</h3>
              <Form >
                 <FormGroup>
                 <Label for ="org">Organization</Label>
                 <Row form>
                    <Col md={8}>
                    <Input type="text" name="org" id="srText"  />
                    </Col>
                    <Col md={4}>
                     <Button type="submit">
                       Search
                     </Button>
                    </Col>
                  </Row>
                  </FormGroup>
                  <FormGroup>
                 <Label for ="org">Language</Label>
                 <Row form>
                    <Col md={8}>
                    <Input type="text" name="lng" id="srText"  />
                    </Col>
                    <Col md={4}>
                     <Button type="submit">
                       Search
                     </Button>
                    </Col>
                  </Row>
                  </FormGroup>
                  <FormGroup>
                 <Label for ="org">Repository url</Label>
                 <Row form>
                    <Col md={8}>
                    <Input type="text" name="repo" id="srText"  />
                    </Col>
                    <Col md={4}>
                     <Button type="submit">
                       Search
                     </Button>
                    </Col>
                  </Row>
                  </FormGroup>
            </Form>
            </Col>
            <Col lg ={7} id="A2" style={{marginTop:'30px'}}>
               <Row>
               
                   <Col md={9}>
                    <FormGroup>
                        <Input type="text" name="Project" id="project" placeholder="Search Project"></Input>
                    </FormGroup>
                   </Col>
                   <Col md ={3}>
                   <Button color="success">Add Project</Button>{' '}
                   </Col>
               
               </Row>


            </Col>
            </Row>
            </div>
        )
    }
}
