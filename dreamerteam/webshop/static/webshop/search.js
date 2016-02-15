$(document).ready(function(){
	var searchService = SearchService(); 

	$('#search-button').click(function() {
		searchService.searchGames($("#search-input").val(), $("#order-by").val(), function(data){
			console.log(data, 'data');
			if(data){
				$('#game-list').html(data); // put data retrieved from search service to html
			} else {
				$('#game-list').html('No games found');
			}
		});
	});

	function SearchService(){
		/* search object (factory pattern) for later easy use of searching games etc */

		var searchGames = function(input, orderBy, callback){
			orderBy = orderBy ? orderBy : 'name'; /* order by name by default */
			$.ajax({
		        type: "GET",
		        url: "/games", 
		        data: {"search_term": input, order: orderBy},
		        success : function(data) {
		            callback(data);
	         	}
			});
		}
		return {
			searchGames: searchGames
		}
	}
});
