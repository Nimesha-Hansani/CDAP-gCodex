import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import RepoStructure from '../Graphs/RepoStructure';
import Comprehension from '../Graphs/CognativeLine';

import {Nav, NavItem, NavLink, Row, Spinner } from 'reactstrap';


import {comprehension} from '../actions/actions';

var ls = require('local-storage');


class AnalyzeMenu extends Component {

    state = {
        activeTab: 'repo_structure',
        comp: false
    }


      repoStructureMethod = (id) =>{
        this.setState({activeTab: id})
      }

      complexityMethod = (id) =>{
        this.setState({activeTab: id})
      }

      comprehensionMethod = (id) =>{
        this.setState({activeTab: id})

        if(this.state.comp === false){
            this.props.comprehension(ls.get('repoName')).then(res => {
                this.setState({comp: true});
                console.log(this.props.comp.data);
              })
        }

      }

      predictionMethod = (id) =>{
        this.setState({activeTab: id})
      }

      bugsMethod = (id) =>{
        this.setState({activeTab: id})
      }

    render() {
        return (
            <div>
                <Nav pills style={{marginTop: '20px'}}>
                    <NavItem className="menu_nav">
                        <NavLink className={this.state.activeTab === 'repo_structure'? 'active': ' '} onClick={()=>this.repoStructureMethod('repo_structure')}>Repo Structure</NavLink>
                    </NavItem>

                    <NavItem className="menu_nav">
                    <NavLink  className={this.state.activeTab === 'complexity'? 'active': ' '} onClick={()=>this.complexityMethod('complexity')}>Complexity</NavLink>
                    </NavItem>

                    <NavItem className="menu_nav"> 
                    <NavLink  className={this.state.activeTab === 'comprehension'? 'active': ' '} onClick={()=>this.comprehensionMethod('comprehension')}>Comprehension</NavLink>
                    </NavItem>

                    <NavItem className="menu_nav">
                    <NavLink  className={this.state.activeTab === 'prediction'? 'active': ' '} onClick={()=>this.predictionMethod('prediction')}>Prediction</NavLink>
                    </NavItem>

                    <NavItem className="menu_nav">
                    <NavLink  className={this.state.activeTab === 'bugs'? 'active': ' '} onClick={()=>this.bugsMethod('bugs')}>Bugs</NavLink>
                    </NavItem>
                
                </Nav>
      
            {(this.state.activeTab === 'repo_structure')?

                <div style={{marginTop: '50px', marginBottom: '100px'}}>

                    {(this.props.analyze.loading === true)? 
                    <Row style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}} >
                        <Spinner color="primary" style={{ width: '3rem', height: '3rem', marginRight: '50px' }}/> <h3 style={{marginTop: '5px'}}>Analyzing...</h3>
                    </Row>
                    
                    
                    : (this.props.analyze.analyze.success === false)? 
                    <h3 style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}}>Please try again later in few minutes...</h3>
                    
                    :  <RepoStructure/>}

                </div>

            : 
            (this.state.activeTab === 'comprehension')?
            
                <div style={{marginTop: '50px', marginBottom: '100px'}}>
                        {(this.props.comp.loading === true)? 
                        <Row style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}} >
                            <Spinner color="primary" style={{ width: '3rem', height: '3rem', marginRight: '50px' }}/> <h3 style={{marginTop: '5px'}}>Analyzing...</h3>
                        </Row>
                        
                        
                        : (this.props.analyze.analyze.success === false)? 
                            <h3 style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}}>Please try again later in few minutes...</h3>
                        
                        :  <Comprehension/>}
                </div>
                    
            
            : null}
               
             




                




            </div>
        )
    }
}


AnalyzeMenu.propTypes = {
    analyze: PropTypes.object.isRequired,
    comp: PropTypes.object.isRequired
  }
  
  
  
  const mapStateToProps = state => ({
    analyze: state.analyze,
    comp:  state.comp
  });
  

export default connect(mapStateToProps, {comprehension})(AnalyzeMenu);