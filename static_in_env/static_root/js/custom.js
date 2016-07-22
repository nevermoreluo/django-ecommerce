function showFlashMessage(message) {
    // var template = "{% include 'alert.html' with message='" + message + "' %}"
    var template = "<div class='container container-alert-flash'>" +
    "<div class='col-sm-3 col-sm-offset-8'> " +
    "<div class='alert alert-success alert-dismissible' role='alert'>" +
    "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
    "<span aria-hidden='true'>&times;</span></button>"
    + message + "</div></div></div>"
    $("body").append(template);
    $(".container-alert-flash").fadeIn();
    setTimeout(function(){
        $(".container-alert-flash").fadeOut();
    }, 1800);

}

jQuery(window).scroll(function() {
        jQuery(this).scrollTop() > 1 ? jQuery("nav").addClass("stick") : jQuery("nav").removeClass("stick"),
            jQuery(this).scrollTop() > 1 ? jQuery(".top-cart").addClass("stick") : jQuery(".top-cart").removeClass("stick")

    }),


    /******************************************
    top search
    ******************************************/

    function(e) {}(jQuery),
    jQuery.extend(jQuery.easing, {}),
    function(e) {
        e.fn.extend({
            accordion: function() {}
        })
    }(jQuery), jQuery(function(e) {
        e(".accordion").accordion(), e(".accordion").each(function() {
            var t = e(this).find("li.active");
            t.each(function(n) {
                e(this).children("ul").css("display", "block"), n == t.length - 1 && e(this).addClass("current")
            })
        })
    }),


    function(e) {
        e.fn.extend({}), jQuery(function() {
            function e() {
                var e = jQuery('.navbar-collapse form[role="search"].active');
                e.find("input").val(""), e.removeClass("active")
            }
            jQuery('.navbar-collapse form[role="search"] button[type="reset"]').on("click keyup", function(t) {
                console.log(t.currentTarget), (27 == t.which && jQuery('.navbar-collapse form[role="search"]').hasClass("active") || "reset" == jQuery(t.currentTarget).attr("type")) && e()
            }), jQuery(document).on("click", '.navbar-collapse form[role="search"]:not(.active) button[type="submit"]', function(e) {
                e.preventDefault();
                var t = jQuery(this).closest("form"),
                    n = t.find("input");
                t.addClass("active"), n.focus()
            }), jQuery(document).on("click", '.navbar-collapse form[role="search"].active button[type="submit"]', function(t) {
                t.preventDefault();
                var n = jQuery(this).closest("form"),
                    i = n.find("input");
                jQuery("#showSearchTerm").text(i.val()), e()
            })
        })
    }(jQuery);
