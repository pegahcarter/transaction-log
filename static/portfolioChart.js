var graphLabels = []
d3.selectAll('#portfolioGraphLabel')
	.each(function(e) {
		graphLabels.push(d3.select(this).text());
	});

var graphData = []
d3.selectAll('#portfolioGraphData')
	.each(function(e) {
		graphData.push(d3.select(this).text());
	});

data = []
for (var i=0; i < graphLabels.length; i++) {
	data.push({
		name: graphLabels[i],
		value: Number(graphData[i])
	});
}


var margin = {
	top: 0,
	right: 0,
	bottom: 0,
	left: 50
}

width = 250 - margin.left - margin.right
height = 200 - margin.top - margin.bottom

// Select body, append SVG area to it, and set the dimensions
var svg = d3.select("#portfolioGraph").append("svg")
	.attr("height", width + margin.left + margin.right)
	.attr("width", height + margin.top + margin.bottom)

var chartGroup = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var x = d3.scaleLinear()
	.range([0, width])
	.domain(d3.extent(data, d => d.value));

var y = d3.scaleBand()
	.range([height, 0])
	.domain(data.map(d => d.name))
	.padding(0.1);

var xAxis = d3.axisBottom(x);
var yAxis = d3.axisLeft(y);

chartGroup.append("g")
	.call(xAxis);

chartGroup.append("g")
	.call(yAxis)
	.attr("transform", "translate(0," + width + ")");

chartGroup.selectAll(".bar")
	.data(data)
	.enter()
	.append("rect")
	.classed("bar", true)
	.attr("x", d => x(d.value))
	.attr("y", d => y(d.name))
	.attr("width", d => height - x(d.value))
	.attr("height", y.bandwidth());
