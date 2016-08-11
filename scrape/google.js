var Scraper = require ('reverse-images-scraper')
  , google = new Scraper.Google();

var ur_el = process.argv[2];

google.list({
    nightmare: {
        show: false
    },
    url: ur_el,
    num: 30
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
