var Scraper = require ('images-scraper')
  , google = new Scraper.Google();

google.list({
    keyword: 'Colosseum',
    detail: true,
    nightmare: {
        show: false
    }
})
.then(function (res) {
	for(x of res)
	{
		console.log(x['url']);
	}
}).catch(function(err) {
    console.log('err', err);
});

google.on('result', function (item) {
});

// cat file | parallel --gnu "wget {}"