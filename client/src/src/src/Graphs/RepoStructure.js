import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';

import $ from 'jquery';

var d3 = require("d3");
class RepoStructure extends Component {

    componentDidMount = ()=>{
        window.addEventListener("message", function (e) {
            var opts = e.data.opts,
                data = e.data.data;
  
            return main(opts, data);
        });
  
        var defaults = {
            margin: { top: 40, right: 0, bottom: 0, left: 0},
            rootname: "TOP",
            format: ",d",
            title: "",
            width: 700,
            height: 600
        };
  
        function main(o, data) {
            var root,
                opts = $.extend(true, {}, defaults, o),
                formatNumber = d3.format(opts.format),
                rname = opts.rootname,
                margin = opts.margin,
                theight = 36 + 16;
  
            $("#chart")
                .width(opts.width)
                .height(opts.height);
            var width = opts.width - margin.left - margin.right,
                height = opts.height - margin.top - margin.bottom - theight,
                transitioning;
  
            // var color = d3.scale.category20c();
            //var color = d3.scale.category10();
  
            var x = d3.scale
                .linear()
                .domain([0, width])
                .range([0, width]);
  
            var y = d3.scale
                .linear()
                .domain([0, height])
                .range([0, height]);
            var area = x * y;
            var colorscale = d3.scale
                .linear()
                .domain([0, height * width])
                .range([0, height * width]);
  
            var colourInterpolator = d3.interpolateHsl("#a89932", "#32a836");
            function colourFunction(d) {
                return colourInterpolator(colorscale(d.value));
            }
  
            var treemap = d3.layout
                .treemap()
                .children(function (d, depth) {
                    return depth ? null : d._children;
                })
                .sort(function (a, b) {
                    return a.value - b.value;
                })
                .ratio((height / width) * 0.5 * (1 + Math.sqrt(5)))
                .round(false);
  
            var svg = d3
                .select("#chart")
                .append("svg")
                //.attr("width", 200)
                //.attr("height", 200)
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.bottom + margin.top)
                .style("margin-left", -margin.left + "px")
                .style("margin.right", -margin.right + "px")
                .append("g")
                .attr(
                    "transform",
                    "translate(" + margin.left + "," + margin.top + ")"
                )
                .style("shape-rendering", "crispEdges");
            $("svg").css({ top: 200, left: 150 });

            var grandparent = svg.append("g").attr("class", "grandparent");
  
            grandparent
                .append("rect")
                .attr("y", -margin.top)
                .attr("width", width)
                .attr("height", margin.top);
  
            grandparent
                .append("text")
                .attr("x", 6)
                .attr("y", 6 - margin.top)
                .attr("dy", ".75em");
  
            if (opts.title) {
                $("#chart").prepend("<p class='title'>" + opts.title + "</p>");
            }
            if (data instanceof Array) {
                root = { key: rname, values: data };
            } else {
                root = data;
            }
  
            
  
            if (window.parent !== window) {
                var myheight =
                    document.documentElement.scrollHeight || document.body.scrollHeight;
                window.parent.postMessage({ height: myheight }, "*");
            }
  
            function initialize(root) {
                root.x =  0;
                root.y = 0;
                root.dx = width;
                root.dy = height;
                root.depth = 0;
            }
  
           
            function accumulate(d) {
                return (d._children = d.values)
                    ? (d.value = d.values.reduce(function (p, v) {
                        return p + accumulate(v);
                    }, 0))
                    : d.value;
            }
  
    
            function layout(d) {
                if (d._children) {
                    treemap.nodes({ _children: d._children });
                    d._children.forEach(function (c) {
                        c.x = d.x + c.x * d.dx;
                        c.y = d.y + c.y * d.dy;
                        c.dx *= d.dx;
                        c.dy *= d.dy;
                        c.parent = d;
                        layout(c);
                    });
                }
            }
  
            function display(d) {
                grandparent
                    .datum(d.parent)
                    .on("click", transition)
                    .select("text")
                    .text(name(d));
  
                var g1 = svg
                    .insert("g", ".grandparent")
                    .datum(d)
                    .attr("class", "depth");
  
                var g = g1
                    .selectAll("g")
                    .data(d._children)
                    .enter()
                    .append("g");
  
                g.filter(function (d) {
                    return d._children;
                })
                    .classed("children", true)
                    .on("click", transition);
  
                var children = g
                    .selectAll(".child")
                    .data(function (d) {
                        return d._children || [d];
                    })
                    .enter()
                    .append("g")

                children
                    .append("rect")
                    .attr("class", "child")
                    .call(rect)
                    .append("title")
  
                    .text(function (d) {
                        return d.key + " (" + formatNumber(d.value) + ")";
                    });
  
  
                children
                    .append("svg:a")
                    .attr("xlink:href", function (d) { return d.url; })  // <-- reading the new "url" property
                    .append("svg:rect");
                children
                    .append("text")
  
                    .attr("class", "ctext")
                    .text(function (d) {
                        return d.key;
                    })
                    .call(text2);
  
                g.append("rect")
                    .attr("class", "parent")
                    .call(rect);
  
                var t = g
                    .append("text")
                    .attr("class", "ptext")
                    .attr("dy", ".75em");
  
                t.append("tspan").text(function (d) {
                    return d.key;
                });
                t.append("tspan")
                    .attr("dy", "1.0em")
                    .text(function (d) {
                        return formatNumber(d.value);
                    });
                t.call(text);
  
                g.selectAll("rect")
                    // .style("fill", function (d) { return color(d.value); });
                    .style("fill", colourFunction);
  
                function transition(d) {
                    if (transitioning || !d) return;
                    transitioning = true;
  
                    var g2 = display(d),
                        t1 = g1.transition().duration(750),
                        t2 = g2.transition().duration(750);
  
                    // Update the domain only after entering new elements.
                    x.domain([d.x, d.x + d.dx]);
                    y.domain([d.y, d.y + d.dy]);
  
                    // Enable anti-aliasing during the transition.
                    svg.style("shape-rendering", null);
  
                    // Draw child nodes on top of parent nodes.
                    svg.selectAll(".depth").sort(function (a, b) {
                        return a.depth - b.depth;
                    });
  
                    // Fade-in entering text.
                    g2.selectAll("text").style("fill-opacity", 0);
  
                    // Transition to the new view.
                    t1.selectAll(".ptext")
                        .call(text)
                        .style("fill-opacity", 0);
                    t1.selectAll(".ctext")
                        .call(text2)
                        .style("fill-opacity", 0);
                    t2.selectAll(".ptext")
                        .call(text)
                        .style("fill-opacity", 1);
                    t2.selectAll(".ctext")
                        .call(text2)
                        .style("fill-opacity", 1);
                    t1.selectAll("rect").call(rect);
                    t2.selectAll("rect").call(rect);
  
                    // Remove the old node when the transition is finished.
                    t1.remove().each("end", function () {
                        svg.style("shape-rendering", "crispEdges");
                        transitioning = false;
                    });
                }
  
                return g;
            }
  
            initialize(root);
            accumulate(root);
            layout(root);
            display(root);


            function text(text) {
                text.selectAll("tspan").attr("x", function (d) {
                    return x(d.x) + 6;
                });
                text
                    .attr("x", function (d) {
                        return x(d.x) + 6;
                    })
                    .attr("y", function (d) {
                        return y(d.y) + 6;
                    })
                    .style("opacity", function (d) {
                        return this.getComputedTextLength() < x(d.x + d.dx) - x(d.x)
                            ? 1
                            : 0;
                    });
            }
  
            function text2(text) {
                text
                    .attr("x", function (d) {
                        return x(d.x + d.dx) - this.getComputedTextLength() - 6;
                    })
                    .attr("y", function (d) {
                        return y(d.y + d.dy) - 6;
                    })
                    .style("opacity", function (d) {
                        return this.getComputedTextLength() < x(d.x + d.dx) - x(d.x)
                            ? 1
                            : 0;
                    });
            }
  
            function rect(rect) {
                rect
                    .attr("x", function (d) {
                        return x(d.x);
                    })
                    .attr("y", function (d) {
                        return y(d.y);
                    })
                    .attr("width", function (d) {
                        return x(d.x + d.dx) - x(d.x);
                    })
                    .attr("height", function (d) {
                        return y(d.y + d.dy) - y(d.y);
                    });
            }
  
            function name(d) {
                return d.parent
                    ? name(d.parent) +
                    " / " +
                    d.key +
                    " (" +
                    formatNumber(d.value) +
                    ")"
                    : d.key + " (" + formatNumber(d.value) + ")";
            }
        }
  
  
  
        
        
       
           
           
                    const branches = this.props.analyze.analyze[0].Branches;
                    console.log(branches);
                    const val = branches.map(bran => {
                        var bname = bran.Branch;
                        //console.log(bname);
                        let sum = 0;
                        let commitval = [];
                        bran.Commits.forEach((commit, index) => {
                            let total = 0;
                            let contentVal = [];
                            commit.Contents.forEach(content => {
                                total = total + content["Source Lines of Code"];
                                contentVal.push({
                                    key: content["Folder Path"],
                                    url: content["Git_Web_Link"],
                                    value: content["Source Lines of Code"]
                                });
                            });
                            commitval.push({
                                key: commit["Commit Date"],
                                value: total,
                                values: contentVal
                            });
                            sum = sum + total;
                        });
                        // console.log(commitval);
  
                        return {
                            key: bran.Branch,
                            value: sum,
                            values: commitval
                        };
  
                    });
                    main(
                        { title: "Repository structure" },
                        { key: "Total Lines of Codes in the Repository", values: val }
                    );
        
    }



    

    render() {
        return (
            <div id="chart"></div>
        )
    }
}

RepoStructure.propTypes = {
    analyze: PropTypes.object.isRequired
  }
  

  
  const mapStateToProps = state => ({
    analyze: state.analyze
  });
  
  export default connect(mapStateToProps)(RepoStructure);