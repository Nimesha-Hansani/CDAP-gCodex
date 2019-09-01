import React from 'react';
import {
  Navbar,
  NavbarBrand, Nav,NavItem,NavLink, Container,Row, Col,Button, Card,CardBody,FormGroup,
  Label,Input ,CardTitle ,CardImg,
  Jumbotron,img
} from 'reactstrap';

export default function home() {
   


    return (
        <div>
         <Navbar class="navBackground" color="info" light expand="md">
            <Container>
                <NavbarBrand id="navToolName" href="/">gCodex</NavbarBrand>
                <Nav className="ml-auto" navbar>
                <NavItem>
                    <NavLink id="sample" href="/">Home</NavLink>
                </NavItem>
                <NavItem>
                    <NavLink id="sample" href="/about">About</NavLink>
                </NavItem>
                <NavItem>
                       <Button  color="danger" href="https://github.com/">Sign Up for Github </Button>
              

                </NavItem>
                </Nav>
            </Container>
         </Navbar>
         

        <Container>
        <Row style={{marginTop: '70px', marginBottom: '60px'}}>
            <Col lg={6}>
            <Card  >
                <CardImg top width="90%" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png" alt=""/>
                <CardBody>
                    <CardTitle style={{color:'green'}}>Sign in to gCodex Account with your Git Account Credintieals</CardTitle>
                    <FormGroup>
                        <Label for="exampleEmail">Username</Label>
                        <Input type="email" name="email" id="exampleEmail" placeholder="Email or Username of your Git Account" />
                    </FormGroup>
                    <FormGroup>
                        <Label for="examplePassword">Password</Label>
                        <Input type="password" name="password" id="examplePassword" placeholder="Password" />
                    </FormGroup>
                    
                    <Button block color ="success" size="lg" href="/usermenu">Log in with Github</Button>

                </CardBody>
            </Card>

            </Col>
            <Col lg={6}>
            <div>
                
                <Jumbotron>
                <h1 className="display-3">Analyze the complexity of your code right away</h1>
                <p className="lead">Identifies the complexity  of source codes through static code complexity analysis,
                bug  detection and finally visualizing the complexity and predict for the future</p>
                </Jumbotron>
            </div>
            </Col>
            
        </Row>
       

         </Container>

        <Row>
          <Col> <img id="animateimg" src = "https://gocode.academy/wp-content/uploads/2018/06/javascript-logo.png " alt ="" style={{width: 'auto'}} /> </Col>
          <Col> <img id="animateimg" src = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" alt =""  style={{width: 'auto'}}/></Col>
          <Col> <img id="animateimg" src = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/PHP-logo.svg/1280px-PHP-logo.svg.png" alt ="" style={{width: 'auto'}}/></Col>
          <Col> <img id="animateimg" src = "https://www.cbronline.com/wp-content/uploads/2016/07/C.png" alt ="" style={{width: 'auto'}}/></Col>
          <Col> <img id="animateimg" src = "https://4.bp.blogspot.com/-gTiw6OELPy0/XJorCue1joI/AAAAAAAACkA/mII85pOuZKYLQlFx6wjkxgkJYrULjv4hQCLcBGAs/s1600/java.png" alt ="" style={{width: 'auto'}}/></Col>
        </Row>

        </div>
    )
}
