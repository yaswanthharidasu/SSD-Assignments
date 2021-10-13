function getPublications(url) {
	// console.log(url);
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", url, true);

	xhttp.onreadystatechange = function () {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var xmlDoc = xhttp.responseXML;
			var articles = xmlDoc.getElementsByTagName("article");
			for (var i = 0; i < articles.length; i++) {
				var author = articles[i].getElementsByTagName("author");
				var title = articles[i].getElementsByTagName("title");
				var ee = articles[i].getElementsByTagName("ee");
				var year = articles[i].getElementsByTagName("year");
				var link;
				for (var j = 0; j < ee.length; j++) {
					link = ee[j].innerHTML;
				}
				var titleText;
				for (var j = 0; j < title.length; j++) {
					titleText = title[j].innerHTML;
				}
				var yearText;
				for (var j = 0; j < year.length; j++) {
					yearText = year[j].innerHTML;
				}
				var authors = ": ";
				for (var j = 0; j < author.length; j++) {
					authors += author[j].innerHTML;
					if (j != author.length - 1) {
						authors += ",";
					}
				}
				var journal =
					'<li><i class="far fa-check-circle"></i><a target=_blank href=' +
					link +
					">" +
					titleText +
					"</a>" +
					authors +
					" (" +
					yearText +
					")";

				$("#journals").append(journal);
			}
			var conferences = xmlDoc.getElementsByTagName("inproceedings");
			for (var i = 0; i < conferences.length; i++) {
				var author = conferences[i].getElementsByTagName("author");
				var title = conferences[i].getElementsByTagName("title");
				var ee = conferences[i].getElementsByTagName("ee");
				var year = conferences[i].getElementsByTagName("year");

				var link;
				for (var j = 0; j < ee.length; j++) {
					link = ee[j].innerHTML;
				}
				var titleText;
				for (var j = 0; j < title.length; j++) {
					titleText = title[j].innerHTML;
				}
				var yearText;
				for (var j = 0; j < year.length; j++) {
					yearText = year[j].innerHTML;
				}
				var authors = ": ";
				for (var j = 0; j < author.length; j++) {
					authors += author[j].innerHTML;
					if (j != author.length - 1) {
						authors += ",";
					}
				}
				var journal =
					'<li><i class="far fa-check-circle"></i><a target=_blank href=' +
					link +
					">" +
					titleText +
					"</a>" +
					authors +
					" (" +
					yearText +
					")";

				$("#conferences").append(journal);
			}
		}
	};

	xhttp.send(null);
}

const urls = [
	"https://dblp.org/pid/r/RaghuReddy.xml",
	"https://dblp.org/pid/44/7025.xml",
	"https://dblp.org/pid/03/4045.xml",
	"https://dblp.org/pid/136/4557.xml",
	"https://dblp.org/pid/08/11295.xml",
	"https://dblp.org/pid/39/7116.xml",
];

for (var i = 0; i < urls.length; i++) {
	getPublications(urls[i]);
}

