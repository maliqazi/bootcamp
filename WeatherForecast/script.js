$(document).ready(function() {
    $('form').submit(function() {
        var location = $('input[name="location"]').val();
        var addHtml = `<h1>${location}</h1>`
        $('div').html(addHtml);
        var url = "http://api.openweathermap.org/data/2.5/weather?q=" + location + "&units=imperial&&appid=967157cd0f77a9b5570aa6361ccf39d0";
        $.get(url, function(res) {
            var tempHTML = `<h3>Temperature: ${res.main.temp}F</h3>`;
            $('div').append(tempHTML);
        }, 'json');
        return false;
    });
});
