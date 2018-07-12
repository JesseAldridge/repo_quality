function time_series(data_objs, element_tag, x_axis_str, y_axis_str) {
  var margin = {top: 20, right: 60, bottom: 60, left: 60}
    , width = 960 - margin.left - margin.right
    , height = 500 - margin.top - margin.bottom;

  var x = d3.scaleTime()
            .domain([
              d3.min(data_objs, function(d) { return d.timestamp; }),
              d3.max(data_objs, function(d) { return d.timestamp; })
            ])
            .range([ 0, width ]);

  var y = d3.scaleLinear()
          .domain([0, d3.max(data_objs, function(d) { return d.value; })])
          .range([ height, 0 ]);

  var chart = d3.select(element_tag)
  .append('svg:svg')
  .attr('width', width + margin.right + margin.left)
  .attr('height', height + margin.top + margin.bottom)
  .attr('class', 'chart');

  console.log('chart:', chart);

  var main = chart.append('g')
  .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
  .attr('width', width)
  .attr('height', height)
  .attr('class', 'main');

  // draw the x axis
  main.append('g')
  .attr('transform', 'translate(0,' + height + ')')
  .attr('class', 'main axis date')
  .call(d3.axisBottom(x));

  main.append("text")
    .attr("transform",
          "translate(" + (width/2) + " ," +
                         (height + margin.top + 20) + ")")
    .style("text-anchor", "middle")
    .text(x_axis_str);

  // draw the y axis
  main.append('g')
  .attr('transform', 'translate(0,0)')
  .attr('class', 'main axis date')
  .call(d3.axisLeft(y));

  // text label for the y axis
  main.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text(y_axis_str);

  var g = main.append("svg:g");

  // g.selectAll("scatter-dots")
  //   .data(data_objs)
  //   .enter().append("svg:circle")
  //       .attr("cx", function (d,i) { return x(d.timestamp); } )
  //       .attr("cy", function (d) { return y(d.value); } )
  //       .attr("r", 4);


  var line = d3.line()
    .x(function(d) { return x(d.timestamp); })
    .y(function(d) { return y(d.value); });

  g.append("path")
      .datum(data_objs)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", 1.5)
      .attr("d", line);

  g.selectAll("text")
    .data(data_objs)
    .enter().append("text")
      .text(function(d) {
          return d.name;
      })
      .attr("x", function(d) {
          return x(d.timestamp) + 5;  // Returns scaled location of x
      })
      .attr("y", function(d) {
          return y(d.value);  // Returns scaled circle y
      })
      .attr("font_family", "sans-serif")  // Font type
      .attr("font-size", "14px")  // Font size
}
