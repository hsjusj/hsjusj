$(function(){
    $(document).on("pjax:end", function(){
        $("#container").fadeIn(200);
    });

    $("#home").click(function(){
        $("#container").hide();
        var url = $(this).attr('url');
        $.pjax({
            url:url,
            type:"POST",
            dataType:"html",
            headers:{"X-CSRFtoken":$.cookie("csrftoken")},
            cache:true,
            storage:true,
            container:"#container"
        })
    });

    $("#archives").click(function(){
        $("#container").hide();
        var url = $(this).attr('url');
        $.pjax({
            url:url,
            type:"POST",
            dateType:"html",
            headers:{"X-CSRFtoken":$.cookie("csrftoken")},
            cache:true,
            storage:true,
            container:"#container"
        })
    });

    $("#about").click(function(){
        $("#container").hide();
        var url = $(this).attr('url');
        $.pjax({
            url:url,
            type:"POST",
            dataType:"html",
            headers:{"X-CSRFtoken":$.cookie("csrftoken")},
            cache:true,
            storage:true,
            container:"#container"
        })
    });

    $(document).on("pjax:start", function(){

    });

    $("#search").click(function(){
        $("#container").hide();
        var url = $(this).attr('url');
        $.pjax({
            url:url,
            type:"POST",
            dateType:"html",
            headers:{"X-CSRFtoken":$.cookie("csrftoken")},
            cache:true,
            storage:true,
            container:"#container"
        });
    });

    $("#container").on("click", ".title a", function(){
        $("#container").hide();
        var url = $(this).attr("addr");
        $.pjax({
            url:url,
            type:"POST",
            dateType:"html",
            headers:{"X-CSRFtoken":$.cookie("csrftoken")},
            cache:true,
            storage:true,
            container:"#container"
        })
    });

    $("#container").on("click", ".search-tag a", function(){
        if ($(this).hasClass("active-tag")){
            return;
        }
        $(".search-tag .active-tag").removeClass("active-tag");
        $(this).addClass("active-tag");
        $("#search-block-container").hide();
        var url = $('.search-tag').attr('url');
        $.ajax({
            url:url,
            type:"POST",
            data:{"tag-name":$(this).attr("tag-name")},
            headers:{"X-CSRFtoken":$.cookie("csrftoken")},
            success:function(data){
                $("#search-block-container").children().remove();
                $("#search-block-container").append(data);
                $("#search-block-container").fadeIn(200);
            }
        })
    });

    $("#container").on("click", ".search-box span", function(){
        $(".active-tag").removeClass("active-tag");
        $("#search-block-container").hide();
        var url = $(this).attr('url');
        $.ajax({
            url:url,
            type:"POST",
            data:{"key-word":$(".search-title").val()},
            headers:{"X-CSRFtoken":$.cookie("csrftoken")},
            success:function(data){
                $("#search-block-container").children().remove();
                $("#search-block-container").append(data);
                $("#search-block-container").fadeIn(200);
            }
        })
    });

    EditormdView = editormd.markdownToHTML("editormd-view", {
        htmlDecode      : "style,script,iframe",  // you can filter tags decode
        emoji           : true,
        taskList        : true,
        tex             : true,  // 默认不解析
        flowChart       : true,  // 默认不解析
        sequenceDiagram : true,  // 默认不解析
    });

    $("#bs-navbar ul li a").click(function(){
        if ($("#bs-navbar").attr("aria-expanded") == "true"){
            $("#navbar-button").click();
        }
    })
});