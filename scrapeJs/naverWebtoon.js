var url='http://comic.naver.com/webtoon/detail.nhn?titleId=119874&no=1141';

var contentSelectors= ['.wt_viewer img'];

var nextLinkSelector= '.btn_next';

var maxPages= 5;

var saveTo= './captures';

var index= 0;
var webpage= require('webpage');
var page= webpage.create();

page.open(url, scrape);

function scrape(status){
	if (status!= 'success'){
		console.log('error-web open'+url);
		phantom.exit();
	}

	console.log(++index+ ': '+ url);

	for(var i=0; i< contentSelectors.length;){
		var clipRect= page.evaluate(function (selector){
			var o= document.querySelector(selector);
			return o? o.getBoundingClientRect(): null;
		}, contentSelectors[i]);

		++i;

		if (clipRect){
			page.clipRect= clipRect;
			page.render(saveTo+ '/'+ index+ '-'+ i+'.png');
		}
	}

	url= page.evaluate(function(selector){
		var o= document.querySelector(selector);
		return o? o.href: null;
	}, nextLinkSelector);

	if(index>= maxPages || !url){
		phantom.exit();
	}
	page.open(url, scrape);
}
