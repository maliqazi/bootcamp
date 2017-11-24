$(document).ready(function() {
    $('img').click(function(){
        var houseName = $(this).attr('id');
        var url = "https://www.anapioficeandfire.com/api/houses?name=house "+houseName;
        $.get(url, function(res){
            //var addHtml = `<h3>${res[0].name}</h3>`;
            $('.innerdetails').html(`<h4>Name: ${res[0].name}</h4>`);
            $('.innerdetails').append(`<h4>Words: ${res[0].words}</h4>`);
            var titlesStr = res[0].titles[0];
            for ( var i=1; i<res[0].titles.length; i++)
            {
                titlesStr = titlesStr + ", " + res[0].titles[i];
            }
            $('.innerdetails').append(`<h4>Titles: ${titlesStr}</h4>`);
        }, "json");
    });
});
