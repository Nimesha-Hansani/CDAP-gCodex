import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
//import '../Functions/Comprehension.js';

import $ from 'jquery';
var d3 = require("d3");

class CognativeLine extends Component {

    componentDidMount = ()=>{
       
        function filterJSON(avgGroupedData, key, value) {
            var result = [];
            avgGroupedData.forEach(function (val, idx, arr) {
              if (val[key] === value) {
      
                result.push(val)
              }
            })
            return result;
        
        }
      
          // Set the dimensions of the canvas / graph
          var margin = { top: 50, right: 20, bottom: 30, left: 160 },
            width = 1200 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;
      
          // Parse the date / time
      
      
          // Set the ranges i changed default 
          var x = d3.time.scale().range([0, width]);
          var y = d3.scale.linear().range([height, 0]);
      
      
      
      
          // Define the axes i changed defalt
          var xAxis = d3.svg.axis().scale(x)
            .orient("bottom").ticks(8)
            //.tickFormat(d3.time.format("%Y"))
            .tickFormat(d3.time.format("%Y-%m-%d"))
      
      
          var yAxis = d3.svg.axis().scale(y)
            .orient("left").ticks(10);
      
          // Define the line
          var stateline = d3.svg.line()
            .interpolate("cardinal")
            .x(function (d) { return x(d.year); })
            .y(function (d) { return y(d.value); });
      
          // Adds the svg canvas
          var svg = d3.select("body")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
          var data;
          // Get the data
        
      
            
          const branches = this.props.comp.data[0].Branches;
            //  console.log(branches);
              branches.forEach(bran => {
                var bname = bran.Branch;
                console.log(bname);
                let cont = [];
                bran.Commits.forEach(commit => {
                  var da = commit["Commit Date"];
                  var ti = commit["Commit Time"];
                  commit.Contents.forEach(content => {
                    cont.push({
                      value: content["Cogitive Weight"],
                      produce: content["Folder Path"],
                      year: da,
                      state: "cognitiveWeight",
                      times: ti,
                      branch: bname
      
                    })
                    cont.push({
                      value: content["Distinct Operators"],
                      produce: content["Folder Path"],
                      year: da,
                      state: "Operators",
                      times: ti,
                      branch: bname
      
      
                    })
      
                    cont.push({
                      value: content["Distinct Identifiers"],
                      produce: content["Folder Path"],
                      year: da,
                      state: "Identifiers",
                      times: ti,
                      branch: bname
      
      
                    })
      
                  });
                });
                // });
      
      
                // group the data
                var groupedData = cont.reduce(function (l, r) {
                  // construct a unique key out of the properties we want to group by
                  var key = r.year + "|" + r.produce + "|" + r.state + "|" + r.branch;
      
                  // check if the key is already known
                  if (typeof l[key] === "undefined") {
                    // init with an "empty" object
                    l[key] = {
                      sum: 0,
                      count: 0
                    };
                  }
      
                  // sum up the values and count the occurences
                  l[key].sum += r.value;
                  l[key].count += 1;
      
                  return l;
                }, {});
      
                //console.log(JSON.stringify(groupedData));
                //{"1|127":{"sum":8,"count":2},"1|129":{"sum":16,"count":2},"2|127":{"sum":14,"count":2},"2|129":{"sum":10,"count":1}}
      
      
                // calculate the averages
                var avgGroupedData = Object.keys(groupedData)
                  // iterate over the elements in <groupedData> and transform them into the "old" format
                  .map(function (key) {
                    // split the constructed key to get the parts
                    var keyParts = key.split(/\|/);
      
                    // construct the "old" format including the average value
                    return {
                      year: keyParts[0],
                      produce: keyParts[1],
                      state: keyParts[2],
                      branch: keyParts[3],
                      value: (groupedData[key].sum / groupedData[key].count)
                    };
                  });
      
                console.log(avgGroupedData);
                // [{"ed_id":1,"el_id":127,"value":4},{"ed_id":1,"el_id":129,"value":8},{"ed_id":2,"el_id":127,"value":7},{"ed_id":2,"el_id":129,"value":10}]
      
      
      
                avgGroupedData.forEach(function (d) {
                 d.year = new Date(d.year);
                    d.branch = d.branch;
                  d.produce = d.produce;
                  d.value = +d.value;
                });
      
                var nest = d3.nest()
                  .key(function (d) {
                    return d.produce;
      
                  })
      
                  .entries(avgGroupedData)
      
                var fruitMenu = d3.select("#inds")
      
                fruitMenu
                  // .append("select")
                  .selectAll("option")
                  .data(nest)
                  .enter()
                  .append("option")
                  //.title("Nested Drop Down")
                  .attr("value", function (d) {
                    return d.key;
                  })
                  .text(function (d) {
                    //var last = str.substring(str.lastIndexOf("/") + 1, str.length);
                    //return d.key.substring(d.key.lastIndexOf("/") + 1, d.key.length);
                    return d.key;
                  })
      
                d3.select('#inds')
                  .on("change", function () {
                    var sect = document.getElementById("inds");
                    console.log(sect);
                    var section = sect.options[sect.selectedIndex].value;
                    console.log(section);
      
                    data = filterJSON(avgGroupedData, 'produce', section);
      
      
                    //debugger
      
                    data.forEach(function (d) {
                      d.value = +d.value;
                      //d.year = parseDate(String(d.year));
                      d.active = true;
                    });
      
      
                    //debugger
                    updateGraph(data);
      
      
                   // jQuery('h1.page-header').html(section);
                  });
      
      
                // generate initial graph
                data = filterJSON(avgGroupedData, 'produce', '/Repo_Clonning/APICall.py');
                updateGraph(data);
      
              });
            

      
          var color = d3.scale.ordinal().range(["#48A36D", "#0096ff", "#ff007e"]);
      
          function updateGraph(data) {
      
      
            // Scale the range of the data
            x.domain(d3.extent(data, function (d) { return d.year; }));
            y.domain([d3.min(data, function (d) { return d.value; }), d3.max(data, function (d) { return d.value; })]);
      
      
            // Nest the entries by state
            const dataNest = d3.nest()
              .key(function (d) { return d.state; })
              .entries(data);
      
      
            var result = dataNest.filter(function (val, idx, arr) {
              return $("." + val.key).attr("fill") !== "#ccc"
              // matching the data with selector status
            })
      
      
            var state = svg.selectAll(".line")
              .data(result, function (d) { return d.key });
      
            state.enter().append("path")
              .attr("class", "line");
      
            state.transition()
              .style("stroke", function (d, i) { return d.color = color(d.key); })
              .attr("id", function (d) { return 'tag' + d.key.replace(/\s+/g, ''); }) // assign ID
              .attr("d", function (d) {
      
                return stateline(d.values)
              });
      
            state.exit().remove();
      
            var legend = d3.select("#legend")
              .selectAll("text")
              .data(dataNest, function (d) { return d.key });
      
            //checkboxes
            legend.enter().append("rect")
              .attr("width", 10)
              .attr("height", 10)
              .attr("x", 0)
              .attr("y", function (d, i) { return 0 + i * 15; })  // spacing
              .attr("fill", function (d) {
                return color(d.key);
      
              })
              .attr("class", function (d, i) { return "legendcheckbox " + d.key })
              .on("click", function (d) {
                d.active = !d.active;
      
                d3.select(this).attr("fill", function (d) {
                  if (d3.select(this).attr("fill") === "#ccc") {
                    return color(d.key);
                  } else {
                    return "#ccc";
                  }
                })
      
      
                var result = dataNest.filter(function (val, idx, arr) {
                  return $("." + val.key).attr("fill") !== "#ccc"
                  // matching the data with selector status
                })
      
                // Hide or show the lines based on the ID
                svg.selectAll(".line").data(result, function (d) { return d.key })
                  .enter()
                  .append("path")
                  .attr("class", "line")
                  .style("stroke", function (d, i) { return d.color = color(d.key); })
                  .attr("d", function (d) {
                    return stateline(d.values);
                  });
      
                svg.selectAll(".line").data(result, function (d) { return d.key }).exit().remove()
      
              })
      
            // Add the Legend text
            legend.enter().append("text")
              .attr("x", 15)
              .attr("y", function (d, i) { return 10 + i * 15; })
              .attr("class", "legend");
      
            legend.transition()
              .style("fill", "#777")
              .text(function (d) { return d.key; });
      
            legend.exit().remove();
      
            svg.selectAll(".axis").remove();
      
            // Add the X Axis
            svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis);
            svg.append("text")
              .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.top + 20) + ")")
              .style("text-anchor", "middle")
              .text(" Commited Date");
      
            // Add the Y Axis
            svg.append("g")
              .attr("class", "y axis")
              .call(yAxis);
      
            svg.append("text")
              .attr("transform", "rotate(-90)")
              .attr("y", 0 - 60)
              .attr("x", 0 - (height / 2))
              .attr("dy", "1em")
              .style("text-anchor", "middle")
              .text("Values")
              .attr("class", "y axis label");
      
      
          };
      
          function clearAll() {
            d3.selectAll(".line")
              .transition().duration(100)
              .attr("d", function (d) {
                return null;
              });
            d3.select("#legend").selectAll("rect")
              .transition().duration(100)
              .attr("fill", "#ccc");
          };
      
          function showAll() {
            d3.selectAll(".line")
              .transition().duration(100)
              .attr("d", function (d) {
                return stateline(d.values);
              });
            d3.select("#legend").selectAll("rect")
              .attr("fill", function (d) {
                if (d.active === true) {
                  return color(d.key);
                }
              })
          };

    }



    render() {
        return (
            <div>
                <div>
                    <select id="inds"><h3>Select the file</h3><br /></select>
                </div>

                <div id="legendContainer" class="legendContainer">
                    <svg id="legend"></svg>
                </div>
            </div>
        )
    }
}

CognativeLine.propTypes = {
    comp: PropTypes.object.isRequired
  }
  

  
  const mapStateToProps = state => ({
    comp: state.comp
  });

export default connect(mapStateToProps)(CognativeLine);