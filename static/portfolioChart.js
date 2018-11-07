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
	top: 10,
	right: 50,
	bottom: 20,
	left: 50
}

width = 600 - margin.left - margin.right
height = 200 - margin.top - margin.bottom

var x = d3.scale.linear()
	.range([0, width])
	.domain(d3.extent(data, d => d.value));

var y = d3.scale.ordinal()
	.domain(data.map(d => d.name))
	.rangeRoundBands([0, height], .2)

var xAxis = d3.svg.axis()
	.scale(x)
	.orient("bottom")
	.tickFormat(d3.format(".0%"));

var yAxis = d3.svg.axis()
	.scale(y)
	.orient("left")
	.tickSize(0)
	.tickPadding(6);

// Select body, append SVG area to it, and set the dimensions
var svg = d3.select("#portfolioGraph").append("svg")
		.attr("height", width + margin.left + margin.right)
		.attr("width", height + margin.top + margin.bottom)

var chartGroup = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

x.domain(d3.extent(data, d => d.value)).nice();
y.domain(data.map(d => d.name));

chartGroup.selectAll(".bar")
		.data(data)
	.enter().append("rect")
		.attr("class", d => "bar bar--" + (d.value < 0 ? "negative" : "positive"))
		.attr("x", d => x(Math.min(0, d.value)))
		.attr("y", d => y(d.name))
		.attr("width", d => Math.abs(x(d.value) - x(0)))
		.attr("height", y.rangeBand()-2)

chartGroup.append("g")
	.attr("class", "x axis")
	.attr("transform", "translate(0," + height + ")")
	.call(xAxis);

chartGroup.append("g")
	.attr("class", "y axis")
	.attr("transform", "translate(" + x(0) + ",0)")
	.call(yAxis);

d3.select('svg')
	.attr("width", "600px")
	.attr("height", "200px")
	.style("border-style", "ridge")

// https://bl.ocks.org/mbostock/2368837
