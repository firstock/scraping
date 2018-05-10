//console.log("node, is there?");
var client= require('cheerio-httpcli');

var url= "http://book.naver.com/";
var param= {};

client.fetch(url, param, function(err, $, res){
	if(err){
		console.log("Error:", err); return;
	}

	//var body= $.html();
	//console.log(body);
	$("a").each(function(idx){
		var text= $(this).text();
		var href= $(this).attr('href');
		console.log(text+":"+href);
	});
});
