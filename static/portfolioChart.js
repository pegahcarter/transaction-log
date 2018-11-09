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
		value: Number(graphData[i])/100
	});
}


var margin = {
	top: 40,
	right: 50,
	bottom: 25,
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
	.tickFormat(d3.format(".0%"))
	.ticks(10);

var yAxis = d3.svg.axis()
	.scale(y)
	.orient("left")
	.tickSize(0)
	.tickPadding(6);

// Select body, append SVG area to it, and set the dimensions
var svg = d3.select("#portfolioGraph").append("svg")
	.attr(
	{
		"height": width + margin.left + margin.right,
		"width": height + margin.top + margin.bottom
	});

var chartGroup = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

x.domain(d3.extent(data, d => d.value)).nice();
y.domain(data.map(d => d.name));

chartGroup.selectAll(".bar")
		.data(data)
	.enter().append("rect")
		.attr(
		{
			"class": d => "bar bar--" + (d.value < 0 ? "negative" : "positive"),
			"x": d => x(Math.min(0, d.value)),
			"y": d => y(d.name),
			"width": d => Math.abs(x(d.value) - x(0)),
			"height": y.rangeBand()-2
		});


chartGroup.append("g")
	.attr(
	{
		"class": "x axis",
		"transform": "translate(0," + height + ")",
	})
	.call(xAxis);

chartGroup.append("g")
	.attr(
	{
		"class": "y axis",
		"transform": "translate(" + x(0) + ",0)"
	})
	.call(yAxis);


chartGroup.append("text")
	.text("Current  Performance")
	.attr(
	{
		"text-anchor": "middle",
		"transform": "translate(-20," + (height/2 - 10) + ")rotate(-90)",
		"font-size": "9pt"
	});

chartGroup.append("text")
	.text("% Change in Current Value")
	.attr(
	{
			"text-anchor": "middle",
			"transform": "translate(" + width/2 + ",-10)"
	});

d3.select("svg")
	.style("border-style", "ridge")
	.attr(
	{
		"width": "600px",
		"height": "200px"
	});
