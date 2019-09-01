import React, { Component } from 'react';
//import {login} from '../Functions/UserFunctions';
import { Alert } from 'reactstrap';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';

import {login, loadSitePage} from '../actions/actions';

//import Axios from 'axios';

import {
    Navbar,
    NavbarBrand, Nav,NavItem,NavLink,Container,Row, Col,Button, Card,CardBody,FormGroup,
    Label,Input ,CardTitle ,CardImg,
    Jumbotron,img
  } from 'reactstrap';

 class Sitepage extends Component {
    
    constructor(props, context){
        super(props, context);
        this.state = {
            EnteredUsername : " ",
            EnteredPassword : " ",
            login: null
        };
        this.submitUserData = this.submitUserData.bind(this);
        this.onChange = this.onChange.bind(this);
    }


    onChange = (event)=>{
        this.setState({[event.target.name] : event.target.value});
    }

    submitUserData(e){
        this.setState({login: null});
      
      e.preventDefault()

      let user = {
        username: this.state.EnteredUsername,
        password: this.state.EnteredPassword
    }
  

      login(user).then(res =>{
          if(res === "False"){ 
            this.setState({login: false});
          }else{
            this.setState({login: true});
            this.props.loadSitePage().then(res => {
                this.props.history.push("/usermenu");
            });
           

            // 
          }
      }); 

    // this.props.loadSitePage(user);
    // console.log(this.props.user);

    }


    

    render(){
        // const {data} = this.props.data;

        return(
            <div>
                <Navbar className="navBackground" color="info" light expand="md">
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

                <Row>
            <Col lg={6}>
            <Card style={{marginTop: '40px',marginLeft : '20px'}} >
                <CardImg top width="90%" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png" alt="Card image cap" />
                <CardBody>
                <CardTitle style={{color:'green'}}>Sign in to gCodex Account with your Git Account Credintieals</CardTitle>

                    {(this.state.login === false) ? <Alert color="danger" >Invalid user login..!</Alert>:null}
                <FormGroup >
                    <Label for="exampleEmail">Username</Label>
                    <Input type="text" name="EnteredUsername" onChange={this.onChange}  placeholder="Email or Username of your Git Account" />
                </FormGroup>
                <FormGroup>
                    <Label for="examplePassword">Password</Label>
                    <Input type="password" name="EnteredPassword" onChange={this.onChange}  placeholder="Password" />
                </FormGroup>
                    <Button block color ="success" size="lg" onClick={this.submitUserData}>
                       Log in with Github
                    </Button>
             
                </CardBody>
            </Card>

            </Col>
            <Col lg={6} >
            <div className
             ="MainPageHitTitle">
                
                <Jumbotron style={{height: "400px"}}>
                <h1 className="display-3">Analyze the complexity of your code right away</h1>
                <p className="lead">Identifies the complexity  of source codes through static code complexity analysis,
                bug  detection and finally visualizing the complexity and predict for the future</p>
                </Jumbotron>
            </div>
            </Col>
            
        </Row>
        <Row>
          <Col> <img id="animateimg" src = "https://gocode.academy/wp-content/uploads/2018/06/javascript-logo.png " alt ="" style={{width: "auto"}} /> </Col>
          <Col> <img id="animateimg" src = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" alt ="" style={{width: "auto"}}/></Col>
          <Col> <img id="animateimg" src = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/PHP-logo.svg/1280px-PHP-logo.svg.png" alt ="" /></Col>
          <Col> <img id="animateimg" src = "https://www.cbronline.com/wp-content/uploads/2016/07/C.png" alt ="" style={{width: "auto"}}/></Col>
          <Col> <img id="animateimg" src = "https://4.bp.blogspot.com/-gTiw6OELPy0/XJorCue1joI/AAAAAAAACkA/mII85pOuZKYLQlFx6wjkxgkJYrULjv4hQCLcBGAs/s1600/java.png" alt ="" style={{width: "auto"}}/></Col>
         </Row>


        
        </div>
        );

    }


}

Sitepage.propTypes = {
    user: PropTypes.object.isRequired,
    // history: PropTypes.shape({
    //     push: PropTypes.func.isRequired
    // }).isRequired
  }
  

const mapStateToProps = state => ({
    user: state.user
});

export default connect(mapStateToProps, {login, loadSitePage})(Sitepage);

