// Toggle highlecting row of selected coins
$('#portfolio tr td').click(function(e) {

	var coinName = $(this).siblings().first().text();
	$('.' + coinName).toggleClass('hideShowTransactions');

	$(this).toggleClass('silver');
	$(this).siblings().not('.redgreenHeavy').toggleClass('silver');
});

// Toggle highlecting row of selected coins
$('rect').click(function(e) {
	var coinIndex = $('rect').index(this);
	var coinName = $('#portfolio tr').eq(coinIndex+1).children().first().text();
	$('.' + coinName).toggleClass('hideShowTransactions');
	$(this).toggleClass('silver');
	//$(this).toggleClass('silver');
	//$(this).siblings().not('.redgreenHeavy').toggleClass('silver');
});
