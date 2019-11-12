import React, { Component } from 'react';
import Plot from 'react-plotly.js';
import PropTypes from 'prop-types';
import { ButtonDropdown, DropdownToggle, DropdownMenu, DropdownItem, Row } from 'reactstrap';

import {connect} from 'react-redux';


class HalstedLineChart extends Component {
    state = {
        dropdownOpen: false,
        itemName: '',
        drop: [],
        cont: [],
        x_axis: [],
        ProgramLength: [],
        Vocabulary: [],
        Effort: [],
        ProgramDifficulty: [],
        data : this.props.complex.data
    }


    toggle = () =>{
        this.setState({dropdownOpen: !this.state.dropdownOpen});
    }

    drawLineChart = (e) =>{
        this.setState({itemName: e.target.value});

        var type = this.state.cont.filter(function (t) {
            return t.Folderpath === e.target.value;
          });

          console.log(type);


          var x = type.map(function(file){
            return file.date;
          });

          var pl = type.map(function(file) {
              return file.ProgramLength;
          })

          var voc = type.map(function(file) {
            return file.Vocabulary;
        })

        var effort = type.map(function(file) {
                return file.Effort;
        })

        var pd = type.map(function(file) {
            return file.ProgramDifficulty;
        })

        

        this.setState({x_axis: x, ProgramLength: pl, Vocabulary: voc, Effort:effort, ProgramDifficulty:pd })


    }



    componentDidMount = () =>{

            const branches = this.props.complex.data[0].Branches;
            let cont = [];
            let drop = [];

            branches.forEach(bran => {
                var bname = bran.Branch;
                bran.Commits.forEach(commit => {
                    var da = commit["Commit Date"];
                    commit.Contents.forEach(content => {

                        cont.push({
                            ProgramLength: content["Program Length"],
                            Vocabulary: content.Vocabulary,
                            ProgramDifficulty: content["Program Difficulty"],
                            Effort: content["Program Effort"],
                            Folderpath: content["Folder Path"],
                            date: da
                        })



                    });

                    commit.Contents.forEach(content => {
                        const foldername = content["Folder Path"]
                        if (drop.indexOf(foldername) == -1) {

                            drop.push(foldername);
                        }


                    });

                });
            });

            this.setState({drop: drop, itemName: drop[0], cont: cont});

    }


    

    render() {
        return (
            <div>
                <Row style={{Right: '10px', textAlign:'center'}}>
                 <h3 style={{marginRight: '20px'}}>Halsted Complexity</h3>

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
                    y:this.state.Vocabulary,
                    type: 'scattergl',
                    marker: {color: 'red'},
                    name: 'Vocabulary '
                    },

                    {x:this.state.x_axis,
                        y:this.state.ProgramLength,
                        type: 'scattergl',
                        marker: {color: 'blue'},
                        name: 'Program Length '
                    }

                 ]}
                
                />


                <Plot
                 data ={[
                    {x:this.state.x_axis,
                    y:this.state.ProgramDifficulty,
                    type: 'scattergl',
                    marker: {color: 'red'},
                    name: 'Program Difficulty '
                    },

                    {x:this.state.x_axis,
                        y:this.state.Effort,
                        type: 'scattergl',
                        marker: {color: 'blue'},
                        name: 'Effort '
                    }

                 ]}
                
                />


            </div>
        )
    }
}


HalstedLineChart.propTypes = {
    complex: PropTypes.object.isRequired
  }
  
  
  
  const mapStateToProps = state => ({
    complex: state.complex
  });
  

export default connect(mapStateToProps)(HalstedLineChart);