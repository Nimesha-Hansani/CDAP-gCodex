import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';

import { TabContent, TabPane, Nav, NavItem, NavLink, Row, Col, Spinner } from 'reactstrap';
import classnames from 'classnames';


import {comprehension} from '../actions/actions';

var ls = require('local-storage');


class AnalyzeMenu extends Component {

    state = {
        activeTab: '1',
        comp: false
    }


    toggle = tab => {
      if(this.state.activeTab !== tab){
       this.setState({activeTab: tab});
      }
    }


    selectRepoForComprehension = async (tab) =>{
        if(this.state.activeTab !== tab){
            this.setState({activeTab: tab});
        }

        if(this.state.comp === false){
            this.props.comprehension(ls.get('repoName')).then(res => {
                this.setState({comp: true});
                console.log(this.props.comp.data);
              })
        }

      }
    

    render() {
        return (
            <div>
                <Nav tabs>

                    <NavItem className="menu_nav">
                    <NavLink
                        className={classnames({ active: this.state.activeTab === '1' })}
                        onClick={() => { this.toggle('1'); }}>
                        Repo Structure
                    </NavLink>
                    </NavItem>

                    <NavItem className="menu_nav">
                    <NavLink
                        className={classnames({ active: this.state.activeTab === '2' })}
                        onClick={() => { this.toggle('2'); }}>
                        Complexity
                    </NavLink>
                    </NavItem>

                    <NavItem className="menu_nav">
                    <NavLink
                        className={classnames({ active: this.state.activeTab === '3' })}
                        onClick={() => { this.selectRepoForComprehension('3'); }}>
                        Comprehension
                    </NavLink>
                    </NavItem>

                    <NavItem className="menu_nav">
                    <NavLink
                        className={classnames({ active: this.state.activeTab === '4' })}
                        onClick={() => { this.toggle('4'); }}>
                        Prediction
                    </NavLink>
                    </NavItem>

                    <NavItem className="menu_nav">
                    <NavLink
                        className={classnames({ active: this.state.activeTab === '5' })}
                        onClick={() => { this.toggle('5'); }}>
                        Bugs
                    </NavLink>
                    </NavItem>

                    </Nav>



                    <TabContent activeTab={this.state.activeTab} style={{marginTop: '50px'}}>

                    <TabPane tabId="1">
                    <Row>
                        <Col sm="12">
                        <h4>Repo Structure</h4>

                        {(this.props.analyze.loading === true) ?
                        <Row><Spinner color="primary" /> <p>{` ${ls.get('repoName')} is analyzing..`}</p></Row>
                        : null}


                        </Col>
                    </Row>
                    </TabPane>

                    <TabPane tabId="2">
                    <Row>
                        <Col sm="12">
                        <h4>Complexity</h4>
                        </Col>
                    </Row>
                    </TabPane>

                    <TabPane tabId="3">
                    <Row>
                        <Col sm="12">
                        <h4>Comprehension</h4>

                        {(this.props.comp.loading === true) ?
                        <Row><Spinner color="primary" /> <p>{` ${ls.get('repoName')} is analyzing..`}</p></Row>
                        : null}


                        </Col>
                    </Row>
                    </TabPane>

                    <TabPane tabId="4">
                    <Row>
                        <Col sm="12">
                        <h4>Prediction</h4>
                        </Col>
                    </Row>
                    </TabPane>

                    <TabPane tabId="5">
                    <Row>
                        <Col sm="12">
                        <h4>Bugs</h4>
                        </Col>
                    </Row>
                    </TabPane>

                    </TabContent>
                
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