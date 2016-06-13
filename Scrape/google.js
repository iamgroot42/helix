var Scraper = require ('reverse-images-scraper')
  , google = new Scraper.Google();

var myArgs = process.argv.slice(2);

var url = myArgs[0]

google.list({
    nightmare: {
        show: false
    },
    url:url
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
