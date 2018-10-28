// When the browser loads, load table
$(function() {
	var coinData = {{ data | safe }};
	console.log(coinData);
});
