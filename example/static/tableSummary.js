d3.selectAll('.redgreenLight').each(function() {
	var tableElement = d3.select(this);
	if (tableElement.text() == " buy ") {
		tableElement.style("background", "LightGreen");
	} else {
		tableElement.style("background", "LightCoral");
	}
});

d3.selectAll('.redgreenHeavy').each(function() {
	tableElement = d3.select(this);
	if (tableElement.text() != 0) {
		tableElement.style("color", "white");
		if (tableElement.text() > 0 ) {
			tableElement.style("background", "Green");
		} else {
			tableElement.style("background", "FireBrick");
		}
	}
});