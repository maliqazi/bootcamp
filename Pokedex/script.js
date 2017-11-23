$(document).ready(function(){
    var base_url="https://pokeapi.co/api/v2/pokemon/";
    for (var i = 1 ; i < 152 ; i++)
    {
        $.get(base_url+i, function(poke_info) {
            var id = poke_info.id;
            var html_str =`<img id=${id} src="${poke_info.sprites.front_default}" alt=""/>`
            $(".images").append(html_str);
        }, "json");

    }

    $('.images').on('click', 'img', function(){
        var id = $(this).attr('id');
        var spriteLoc = $(this).attr('src');
        $.get(base_url+id, function(poke_info){
            var html_str = `<h1>${poke_info.forms[0].name}</h1>
                            <img id=${id} src="${poke_info.sprites.front_default}" alt=""/>
                           `
            var html_str2 = "<ul>Types</ul>";
            for (var j=0; j < poke_info.types.length; j++)
            {
                var html_str2 = html_str2 + `<li>${poke_info.types[j].type.name}</li>`
            }
            var html_str3 = `<h5>Height</h5>
                             <p>${poke_info.height}</p>
                             <h5>Weight</h5>
                             <p>${poke_info.weight}</p>
                            `
            var full_html = html_str+html_str2+html_str3;
            $(".redbox").html(full_html);
        }, "json");
    });
});
