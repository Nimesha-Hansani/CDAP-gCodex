import React, { Component } from 'react';
import Plot from 'react-plotly.js';
import PropTypes from 'prop-types';
import { ButtonDropdown, DropdownToggle, DropdownMenu, DropdownItem, Row } from 'reactstrap';

import $ from 'jquery';

import {connect} from 'react-redux';


class LocLineChart extends Component {
    state = {
        dropdownOpen: false,
        itemName: '',
        drop: [],
        cont: [],
        x_axis: [],
        SLOC: [],
        FLOC: [],
        data : this.props.analyze.analyze[0]
    }


    toggle = () =>{
        this.setState({dropdownOpen: !this.state.dropdownOpen});
    }

    drawLineChart = (e) =>{
        this.setState({itemName: e.target.value});

        var type = this.state.cont.filter(function (t) {
            return t.type === e.target.value;
          });

          var x = type.map(function(file){
            return file.date;
          });

          var sloc = type.map(function(file) {
              return file.SLOC;
          })

          var floc = type.map(function(file) {
            return file.FLOC;
        })

        this.setState({x_axis: x, SLOC: sloc, FLOC: floc })


    }



    componentDidMount = () =>{

            const branches = this.props.analyze.analyze[0].Branches;
            //console.log(branches);
            let cont = [];
            let drop = [];

            branches.forEach(bran => {
                var bname = bran.Branch;
                //console.log(bname);
                
                bran.Commits.forEach(commit => {

                    var da = commit["Commit Date"];
                    //var ti = commit["Commit Time"];
                    commit.Contents.forEach(content => {

                        cont.push({
                            SLOC: content["Source Lines of Code"],
                            //CommentLines: content["Comment Lines"],
                            FLOC: content["File Lines of Code"],

                            type: content["Folder Path"],
                            date: da
                        })

                    });



                    commit.Contents.forEach(content =>{
                        var type = content["Folder Path"];
                        if(drop.indexOf(type) == -1){
                            drop.push(type);
                        }

                    })

                });
                
            });

            this.setState({drop: drop, itemName: drop[0], cont: cont});
    }


    

    render() {
        return (
            <div>
                <Row style={{Right: '10px', textAlign:'center'}}>
                 <h3 style={{marginRight: '20px'}}>Lines of Codes Changing Over Time</h3>

                 <ButtonDropdown isOpen={this.state.dropdownOpen} toggle={this.toggle}>
                    <DropdownToggle caret>Choose a file</DropdownToggle>
                    <DropdownMenu>

                        {
                            this.state.drop.map(name =>(
                                <DropdownItem key={name}  action value={name} onClick={this.drawLineChart}>
                                  {name}
                                </DropdownItem>))
                        }



                    </DropdownMenu>
                </ButtonDropdown>
                </Row>

                   


                <Plot
                 data ={[
                    {x:this.state.x_axis,
                    y:this.state.SLOC,
                    type: 'scattergl',
                    marker: {color: 'red'},
                    name: 'SLOC '
                    },

                    {x:this.state.x_axis,
                        y:this.state.FLOC,
                        type: 'scattergl',
                        marker: {color: 'blue'},
                        name: 'FLOC '
                    }

                 ]}
                
                />


            </div>
        )
    }
}


LocLineChart.propTypes = {
    analyze: PropTypes.object.isRequired
  }
  
  
  
  const mapStateToProps = state => ({
    analyze: state.analyze
  });
  

export default connect(mapStateToProps)(LocLineChart);