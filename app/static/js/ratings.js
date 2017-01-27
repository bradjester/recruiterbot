(function($){

    $.fn.ratings = function(options){
        var settings = $.extend({
            target : this.selector,
            stars : 1,
            range : [],
            count : 1,
            default_stars : 0,
            on_select : null
        }, options );

        var ratings = {
            target: settings.target,
            star : "rate_star",
            stars: settings.stars,
            range: settings.range,
            count: settings.count,
            checked_class : "checked",
            active_element : null,
            input_class : "get_rate",
            default_stars : settings.default_stars,
            on_select : settings.on_select
        };

        append_stars(ratings);
        traverse(ratings);

        return this;
    };

    // append stars to the selector element
    function append_stars(ratings){
        $(ratings.target).each(function(){

            if (ratings.stars > 1 && ratings.range == '' && ratings.count == 1){
                for (var i = 1; i <= ratings.stars; i++){
                   $(this).append("<span class='" + ratings.star +"' data-value='" + i + "'></span>");
                }
                $(this).append("<input type='hidden' class='" + ratings.input_class + "' value=''>");
            } else if (ratings.stars > 1 && ratings.range == '' && ratings.count > 1){

                var i = 1, step = i;
                for (i; i <= ratings.stars; i++){
                    $(this).append("<span class='" + ratings.star +"' data-value='" + step + "'></span>");  // set data-value attributes with incremented steps
                    step += ratings.count;
                }
                $(this).append("<input type='hidden' class='" + ratings.input_class + "' value=''>");
            }

            if (ratings.range && ratings.range.length == 2 && ratings.count == 1){

                var iteration = 0;
                for (var j = ratings.range[0]; j < ratings.range[1]; j++){
                    $(this).append("<span class='" + ratings.star +"' data-value='" + j + "'></span>"); // set data-value attributes
                    iteration++;
                }
                $(this).append("<input type='hidden' class='" + ratings.input_class + "' value=''>");

            } else if (ratings.range && ratings.range.length == 2 && ratings.count > 1){

                var j = ratings.range[0], step  = j, iteration = 0;
                for (j; j < ratings.range[1]; j++){
                    $(this).append("<span class='" + ratings.star +"' data-value='" + step + "'></span>");  // set data-value attributes with incremented steps
                    step += ratings.count;
                    iteration++;
                }
                $(this).append("<input type='hidden' class='" + ratings.input_class + "' value=''>");
            }

        });
    }

    // iterate over appended elements
    function traverse(ratings){

        if (ratings.stars) {

            var star_id;

            $(ratings.target + ' .' + ratings.star).each(function (key, value) {

                $(this).hover( // change star's color after mouse hover
                    function () {
                        $(this).prevAll().andSelf().addClass('over');
                    },
                    function () {
                        $(this).prevAll().andSelf().removeClass('over');
                    }
                );

                $(this).on('click', function () { // get rate after click
                    star_id = $(this).attr('data-value');
                    $(this).siblings("input." + ratings.input_class).val(star_id);
                    $(this).prevAll().andSelf().addClass(ratings.checked_class);
                    $(this).nextAll().removeClass(ratings.checked_class);
                    ratings.active_element = $(this).parent();
                    if (ratings.on_select && typeof ratings.on_select === "function"){

                        ratings.on_select(star_id);
                    }
                });

            });

            $(ratings.target).each(function (key, value) {

                if (ratings.default_stars > 0 && key <= ratings.default_stars &&
                    ratings.stars >= ratings.default_stars){

                    $(ratings.target).find("input." + ratings.input_class).attr('default-stars', ratings.default_stars);
                    var default_selected = $(ratings.target).find("input." + ratings.input_class).attr('default-stars');
                    var set_last_default;

                    for (var k = 0; k < default_selected; k++){

                        $(this).find('.rate_star').eq(k).addClass(ratings.checked_class);
                    }
                    set_last_default = $(ratings.target).find('span.checked:last').attr('data-value');
                    $(this).find("input." + ratings.input_class).val(set_last_default);
                }

                if (ratings.stars <= ratings.default_stars){
                    console.warn('The number of stars in a row should be bigger than the number of default stars.');
                }
                if (ratings.default_stars < 0){
                    console.warn('The number of default stars should be bigger than 0.');
                }
                if (ratings.key >= ratings.default_stars){
                    console.warn('The number of Rows should be less than the number of default stars.');
                }
            });

            return star_id;
        }

    }

}(jQuery));