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

var x = d3.scale.linear()
	.range([0, width])
	.domain(d3.extent(data, d => d.value));

var y = d3.scale.ordinal()
	.domain(data.map(d => d.name))
	.rangeRoundBands([0, height])
	.padding(0.1);

var xAxis = d3.svg.axis()
	.scale(x)
	.orient("bottom");

var yAxis = d3.svg.axis()
	.scale(y)
	.orient("left")
	.tickSize(0)
	.tickPadding(6);

chartGroup.append("g")
	.call(xAxis);

chartGroup.append("g")
	.call(yAxis)
	.attr("transform", "translate(0," + width + ")");

chartGroup.selectAll(".bar")
		.data(data)
	.enter().append("rect")
		.attr("class", "bar")
		.attr("x", d => x(Math.min(0, d.value)))
		.attr("y", d => y(d.name))
		.attr("width", d => Math.abs(x(d.value) - x(0)))
		.attr("height", y.rangeBand());


// https://bl.ocks.org/mbostock/2368837
