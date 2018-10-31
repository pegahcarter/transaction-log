$('.redgreenLight').each(function() {
	if ($(this).text() == ' buy ') {
		$(this).css('background', 'LightGreen');
	} else {
		$(this).css('background', 'LightCoral');
	}
});

$('.redgreenHeavy').each(function() {
	if ($(this).text() != 0) {
		$(this).css('color', 'white');
		if ($(this).text() > 0 ) {
			$(this).css('background', 'Green');
		} else {
			$(this).css('background', 'FireBrick');
		}
	}
});


// Toggle highlecting row of selected coins
$('#portfolioTableBody tr td').click(function(e) {

	var coinName = $(this).siblings().first().text().trim();
	$('#transactionsTable tbody .' + coinName).toggleClass('hideShowTransactions');

	$(this).toggleClass('silver');
	$(this).siblings().not('.redgreenHeavy').toggleClass('silver');
	if ($(this).hasClass('silver')) {
		console.log('this is silver');
	} else {
		console.log('this is not silver');
	}
});
