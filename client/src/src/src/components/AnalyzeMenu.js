import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';

import {Nav, NavItem, NavLink, Row, Spinner, Dropdown, DropdownItem, DropdownToggle, DropdownMenu} from 'reactstrap';

import RepoStructure from '../Graphs/RepoStructure';
import Comprehension from '../Graphs/CognativeLine';
import LOClinechart from '../Graphs/LocLineChart';
import HalstedLineChart from '../Graphs/HalstedLineChart';

import {comprehension, halsted, analyzing, prediction} from '../actions/actions';





var ls = require('local-storage');


class AnalyzeMenu extends Component {

    state = {
        activeTab: 'repo_structure',
        comp: false,
        complexity: 'Complexity',
        dropdownOpen: false
    }

    
    
      toggle = () =>{
        this.setState({dropdownOpen: !this.state.dropdownOpen});
      }

      LOClinechart = (id) =>{
        this.setState({complexity: 'LOC Line Chart', activeTab: id});
        this.props.analyzing(ls.get('repoName'));
      }

      Hulstedlinechart = (id) =>{
        this.setState({complexity: 'Hulsted Line Chart', activeTab: id});
        this.props.halsted(ls.get('repoName'));
      }

      Cyclomatislinechart = () =>{
        this.setState({complexity: 'Cyclomatis Line Chart'})
      }



      repoStructureMethod = (id) =>{
        this.setState({activeTab: id, complexity: 'Complexity'});
        this.props.analyzing(ls.get('repoName'));
      }


      comprehensionMethod = (id) =>{
        this.setState({activeTab: id, complexity: 'Complexity'});
        this.props.comprehension(ls.get('repoName'));
      }




      predictionMethod = (id) =>{
        this.setState({activeTab: id, complexity: 'Complexity'});
        this.props.prediction(ls.get('repoName'));
      }

      bugsMethod = (id) =>{
        this.setState({activeTab: id, complexity: 'Complexity'})
      }

    render() {
        return (
            <div>
                <Nav pills style={{marginTop: '20px'}}>
                    <NavItem className="menu_nav">
                        <NavLink className={this.state.activeTab === 'repo_structure'? 'active': ' '} onClick={()=>this.repoStructureMethod('repo_structure')}>Repo Structure</NavLink>
                    </NavItem>


                    <Dropdown nav isOpen={this.state.dropdownOpen} toggle={this.toggle} active>
                    <DropdownToggle nav >{this.state.complexity}</DropdownToggle>
                    <DropdownMenu>
                      <DropdownItem  onClick={()=>this.LOClinechart('loc_line')} >LOC Line Chart</DropdownItem>
                      <DropdownItem onClick={()=>this.Hulstedlinechart('hulsted')} >Halstead Line Chart</DropdownItem>
                      <DropdownItem onClick={()=>this.Cyclomatislinechart('cyclomatis')} >Cyclomatis Line Chart</DropdownItem>
                    </DropdownMenu>
                  </Dropdown>






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
                        
                        
                        : (this.props.comp.data.success === false)? 
                            <h3 style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}}>Please try again later in few minutes...</h3>
                        
                        :  <Comprehension/>}
                </div>
                    
            
            : (this.state.activeTab === 'loc_line')?
                    
            <div style={{marginTop: '50px', marginBottom: '100px'}}>
                        {(this.props.analyze.loading === true)? 
                        <Row style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}} >
                            <Spinner color="primary" style={{ width: '3rem', height: '3rem', marginRight: '50px' }}/> <h3 style={{marginTop: '5px'}}>Analyzing...</h3>
                        </Row>
                        
                        
                        : (this.props.analyze.analyze.success === false)? 
                            <h3 style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}}>Please try again later in few minutes...</h3>
                        
                        :  <LOClinechart/>}
                </div>
            
            : (this.state.activeTab === 'hulsted')?
                    
                <div style={{marginTop: '50px', marginBottom: '100px'}}>
                        {(this.props.complex.loading === true)? 
                        <Row style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}} >
                            <Spinner color="primary" style={{ width: '3rem', height: '3rem', marginRight: '50px' }}/> <h3 style={{marginTop: '5px'}}>Analyzing...</h3>
                        </Row>
                        
                        
                        : (this.props.analyze.analyze.success === false)? 
                            <h3 style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}}>Please try again later in few minutes...</h3>
                        
                        :  <HalstedLineChart/>}
                </div>
                :(this.state.activeTab === 'prediction')?
                    
                <div style={{marginTop: '50px', marginBottom: '100px'}}>
                        {(this.props.predict.loading === true)? 
                        <Row style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}} >
                            <Spinner color="primary" style={{ width: '3rem', height: '3rem', marginRight: '50px' }}/> <h3 style={{marginTop: '5px'}}>Analyzing...</h3>
                        </Row>
                        
                        
                        : (this.props.analyze.analyze.success === false)? 
                            <h3 style={{marginTop: '100px', marginLeft: '150px', position: 'absolute'}}>Please try again later in few minutes...</h3>
                        
                        :  
                        // <HalstedLineChart/>
                        <h2>done</h2>}
                </div>
                :null}
               
             




                




            </div>
        )
    }
}


AnalyzeMenu.propTypes = {
    analyze: PropTypes.object.isRequired,
    comp: PropTypes.object.isRequired,
    complex: PropTypes.object.isRequired,
    predict: PropTypes.object.isRequired
  }
  
  
  
  const mapStateToProps = state => ({
    analyze: state.analyze,
    comp:  state.comp,
    complex:  state.complex,
    predict: state.predict,
  });
  

export default connect(mapStateToProps, {comprehension, analyzing, halsted, prediction})(AnalyzeMenu);