const $ = require('jquery');

$(() => {
    console.log('hello');
    $.getJSON('/problems/', (dic) => {
        dic['problems'].forEach((problem, idx) => {
            console.log(problem);
            $('.problems').append(`<li><p>${problem["statement"]}</p><input type='text' class="flag${idx}"><button class="button${idx}">submit</button></li>`);
            $(`.button${idx}`).click(() => {
                const d = {"flag": $(`.flag${idx}`).val(), "name": $(".name").val()};

                $.post(`/problems/${idx}`, d, (d) => {
                    const data = JSON.parse(d);
                    if (data["Status"] == 1) {
                        $('.main').append('<p class="succeeded">Succeeded</p>');
                    }
                    else{
                        $('.main').append('<p class="failure">Failed</p>');
                    }
                });
            });
        });
    });
});
