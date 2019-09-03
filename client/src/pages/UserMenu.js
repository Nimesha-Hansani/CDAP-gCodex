import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';

import {login, loadSitePage, searching, analyzing} from '../actions/actions';
import {
    Navbar,Container,NavbarBrand,NavLink,NavItem,Nav,Row,
    Col,Button,Form,FormGroup,Input,
    Label,ListGroup,ListGroupItem, ButtonGroup, Jumbotron, Spinner} from 'reactstrap';
 
// var ls = require('local-storage');




class UserMenu extends Component {

  constructor(props){
    super(props);
    this.state = {
        searchResults : null,
        searchType : null,
        keyword: null
    };
  }

  signOut = () => {
    localStorage.removeItem('state');
    this.props.history.push("/Sitepage");
  }

  setSearch = (event) =>{
    this.setState({searchType: event.target.name, keyword: event.target.value});
  }

  searchRepo = ()=>{
    this.setState({searchResults : null});
    this.props.searching(this.state.searchType, this.state.keyword).then(res => {
      if(this.props.search.result === null){
        this.setState({searchResults: false})
      }else{
        this.setState({searchResults: true})
      }
    });
  }


  selectRepoforAnalyze = (event) =>{
    this.props.analyzing(event.target.value).then(res => {
      console.log(this.props.analyze.analyze);
    })
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
                    <NavLink id="sample" href="/about">{this.props.user.data.userName}</NavLink>
                </NavItem>
                <NavItem>
                   <img src={this.props.user.data.avatar} alt="Avatar" className="avatar"/>
                </NavItem>
                <NavItem style={{marginTop:'8px'}}>
                        <Button color="secondary" onClick={this.signOut}>Sign Out</Button>{' '}
                </NavItem>
                </Nav>
            </Container>
            </Navbar>
          
         
          <Container  fluid>
          <Row style={{marginTop: '50px'}}>
            
            <Col xs="6" sm="3">
              <ListGroup>
                <ListGroupItem active tag="button" action>Your current projects</ListGroupItem>

                  {(this.props.user.data.repoList !== null) ? 
                  
                    this.props.user.data.repoList.map(name =>(
                      <ListGroupItem key={name} tag="button" action value={name} onClick={this.selectRepoforAnalyze}>
                        {name}
                      </ListGroupItem>
                    )):
                      
                    <ListGroupItem>You have no any Repositories</ListGroupItem>
                  }
              </ListGroup>
              
            </Col>
            
            <Col xs="6" sm="6">
             
                <div>
                  <Jumbotron>
                    <h1 className="display-3">gCodex</h1>
                    <p className="lead">Analyze the complexity of your code right away here..</p>
                    <hr className="my-2" />
                    <p>Select or search Repositories for Analyze..</p>
                    
                    <div style={{padding: '50px 5px 0 0'}}>
                    <ButtonGroup size="lg" style={{width:'200px'}}>
                      <Button color="primary">Repo Structure</Button>
                      <Button color="primary">Complexity</Button>
                      <Button color="primary">Comprehension</Button>
                      <Button color="primary">Bugs</Button>
                      <Button color="primary">Prediction</Button>
                    </ButtonGroup>
                    </div>
                  </Jumbotron>
                
              </div>
            </Col>
            
            <Col xs="6" sm="3">
              <div style={menuStyle}>
              <h3 className="SearchText">Search Repositories</h3>
                  <Form >
                    <FormGroup>
                      <Label for ="org">Language</Label>
                      <Input type="text" name="language" onChange={this.setSearch} />
                      <Label for ="org">Repository url</Label>
                      <Input type="text" name="repoURL" id="srText"  onChange={this.setSearch}/>
                    </FormGroup>
                    <hr/>
                    <FormGroup>
                      <Input type="text" placeholder="Or search your projects.."></Input>
                    </FormGroup>

                    <FormGroup><Button block onClick={this.searchRepo}>Search</Button></FormGroup>
                  </Form>
              </div>

              {(this.props.search.loading === true) ? <Row>
              <h4 style={{marginRight: '20px'}}>Searching...</h4>
              <Spinner color="primary" /></Row>
              : null }
              
              {(this.state.searchResults !== null) ?
              <div>
                <h5>Search results :
                  {(this.state.searchResults === false) ? <h5><i>Items not found</i></h5>: null}
                  
                  </h5>
                <div className="card example-1 square scrollbar-cyan bordered-cyan">
              <ListGroup>    
                  {this.props.search.result.RepoList.map(name =>(
                    <ListGroupItem key={name} tag="button" action value={name} onClick={this.selectRepoforAnalyzes}>
                      {name}
                    </ListGroupItem>
                  ))}

              </ListGroup>
              </div>

              </div>: null}
               
            </Col>
              
          </Row>
          </Container>
        

          
        </div>
        )
    }
}

UserMenu.propTypes = {
  user: PropTypes.object.isRequired,
  search: PropTypes.object.isRequired,
  analyze: PropTypes.object.isRequired
}


const menuStyle = {
  paddingTop:'20px',
  backgroundColor: 'rgba(23, 162, 184, 0.25)',
  borderRadius: '5px',
  padding: '20px',
  height: 'auto',
  marginBottom: '20px'
}


const mapStateToProps = state => ({
  user: state.user,
  search: state.search,
  analyze: state.analyze
});

export default connect(mapStateToProps, {login, loadSitePage, searching, analyzing})(UserMenu);
