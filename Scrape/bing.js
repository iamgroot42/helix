var Scraper = require ('images-scraper')
  , bing = new Scraper.Bing();

bing.list({
    keyword: 'Colosseum',
    detail: true
})
.then(function (res) {
    for(x of res)
    {  
        console.log(x['url']);
    }
}).catch(function(err) {
    console.log('err',err);
})

// cat file | parallel --gnu "wget {}"