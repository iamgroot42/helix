// var Scraper = require ('images-scraper')
//   , google = new Scraper.Google();

// google.list({
//     keyword: 'Pyramids',
//     detail: true,
//     nightmare: {
//         show: false
//     }
// })
// .then(function (res) {
// 	for(x of res)
// 	{
// 		console.log(x['url']);
// 	}
//     // console.log('first 25 results from google', res);
// }).catch(function(err) {
//     console.log('err', err);
// });

// // you can also watch on events
// google.on('result', function (item) {
//     // console.log('out', item);
// });


var Scraper = require ('images-scraper')
  , bing = new Scraper.Bing();

bing.list({
    keyword: 'Taj Mahal',
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