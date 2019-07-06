$(function(){
    $(".selected-btn").click(function(){
        if ($(".selected-menu").css("display") == "none"){
            $(".selected-menu").css("display", "block");
        }else{
            $(".selected-menu").css("display", "none");
        }
    });

    $(".selected-menu .selected-tag").click(function(){
        if ($(this).hasClass("selected-active")){
            $(this).removeClass("selected-active");
            $(this).find("span").remove();
        }else{
            $(this).append($("<span style=\"float:right;\" class=\"glyphicon glyphicon-ok\" aria-hidden=\"true\"></span>"));
            $(this).addClass("selected-active");
        }
    });

    $(".add-tags-btn").click(function(){
        $(this).parent().parent().append('<li><input class="form-control" type="text" placeholder="new tag..."></li>');
    });

    $(".del-tags-btn").click(function(){
        $(".selected-menu li:last input").parent().remove();
    });

    $("body").on("click", ".remove-tag", function(){
        $(this).parent().remove();
    })
});