/**
 * Created by Administrator on 2016/9/20.
 */

// 初始化模态框
$(function () {
        $("#Login-Register-Modal").modal({show:false,backdrop:false,keyboard:false});
        $("#Add-Item-Modal").modal({show:false,backdrop:false,keyboard:false});
    });
// 判断是否用户已经登录，决定发布按钮弹出的模块框
$("#show-pub-box").click(function () {
    $.ajax({
        url:"/login_confirm/",
        type:"POST",
        dataType:'json',
        data:{
            "type":"login_confirm",
        },
        success:function (data) {
            if(data.status){
                $("#Add-Item-Modal").modal('show');
            }else{
                $("#Login-Register-Modal").modal('show');
            }
        },
    });
});

    
// 发布内容导航切换
$("#Add-Item-Modal ul.nav-tabs li").click(function () {
    $(this).addClass("active");
    $(this).siblings().removeClass("active");
    var text = $(this).children().first().text()
    if(text == "链接"){
        $("#AddLink").removeClass("hidden");
        $("#AddText").addClass("hidden");
        $("#AddPic").addClass("hidden");

    }else if(text == "文字"){
        $("#AddText").removeClass("hidden");
        $("#AddLink").addClass("hidden");
        $("#AddPic").addClass("hidden");

    }else if(text == "图片"){
        $("#AddPic").removeClass("hidden");
        $("#AddLink").addClass("hidden");
        $("#AddText").addClass("hidden");
    }
});

// 获取标题按钮
$("#gain_title").click(function () {
    var thus =$(this);
    $(this).text("内容获取中...");
    $(this).addClass("disabled");
    var article_url = $("#Link").val();
    $.ajax({
        url:"/gain/",
        type:"POST",
        dataType:'json',
        data:{
            "url":article_url,
        },
        success:function (data) {
            if(data.status){
                thus.text("获取标题");
                thus.removeClass("disabled");
                $("#publish").removeClass("disabled");
                var title = data.message[0];
                var abstract = data.message[1];
                $("#Title").val(title);
                $("#Abstract").text(abstract);
            }else{
                thus.text("获取标题");
                thus.removeClass("disabled");
                $("label[for='Link']").after("&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: red;" + "font-size: 14px'>" + data.message + "\</span>");
                window.setTimeout('$("label+span").remove();',2000);
            }
        },
    });
});

// 选择发布的类型
$("#AddLink li[role='presentation'] span").click(function () {
    $(this).addClass("selected btn-primary").removeClass("btn-default");
    $(this).parent().siblings().children().removeClass("selected btn-primary").addClass("btn-default");
});
// 重置发布表单的内容
$("#clear-link").click(function () {
    $("#Link").val('');
    $("#Title").val('');
    $("#Abstract").text('');
    $("#publish").addClass("disabled");
});
// 当url变更时，重置表单，发布按钮不可用
$("#Link").change(function () {
    $("#Title").val('');
    $("#Abstract").text('');
    $("#publish").addClass("disabled");
});
// 发布新51区内容
$("#publish").click(function () {
    if($(this).hasClass("disabled")){
        return false;
    }
    var type = $("#AddLink li[role='presentation'] span.selected").text();
    var url = $("#Link").val();
    var title = $("#Title").val();
    var abstract = $("#Abstract").text();
    $.ajax({
        url:"/publish/",
        type:"POST",
        dataType:'json',
        data:{
            "type":type,
            "url":url,
            "title":title,
            "abstract":abstract,
        },
        success:function (data) {
            if(data.status){
                $("#myModalLabel-2+span").text("发布成功！返回主页...").css({"color":"orange","font-size":"14px"});
                window.setTimeout("window.location.href='/index/'",1000);
            }else{
            }
        },
    });
});


/*
发布文本的js代码 */

// 选择发布的类型
$("#AddText li[role='presentation'] span").click(function () {
    $(this).addClass("selected btn-primary").removeClass("btn-default");
    $(this).parent().siblings().children().removeClass("selected btn-primary").addClass("btn-default");
});
// 重置发布表单的内容
$("#clear-text").click(function () {
    $("#add-text").val('');
    $("#publish-text").addClass("disabled");
});
// 当文本区域有内容时发布按钮可用
$("#add-text").keyup(function () {
    if($(this).val().length > 0){
        $("#publish-text").removeClass("disabled");
    }else{
        $("#publish-text").addClass("disabled");
    }
});
// 发布新段子
$("#publish-text").click(function () {
    if($(this).hasClass("disabled")){
        return false;
    }
    if($("#add-text").val().length >= 256){
        $("#myModalLabel-2+span").text("不得超过256个字...").css({"color":"orange","font-size":"14px"});
        return false;
    }
    var type = $("#AddText li[role='presentation'] span.selected").text();
    var title = $("#add-text").val();
    $.ajax({
        url:"/publish_text/",
        type:"POST",
        dataType:'json',
        data:{
            "type":type,
            "title":title,
        },
        success:function (data) {
            if(data.status){
                $("#myModalLabel-2+span").text("发布成功！返回主页...").css({"color":"orange","font-size":"14px"});
                window.setTimeout("window.location.href='/index/'",1000);
            }else{
            }
        },
    });
});





// 推荐功能，点击一次推荐+1，再次点击推荐-1，未登陆不可推荐
$("div.article li span.recommend").click(function () {
    var thus = $(this);
    var title = $(this).parent().parent().parent().parent().children().first().children().first().text();
    $.ajax({
        url:"/recommend/",
        type:"POST",
        dataType:'json',
        data:{
            "title":title,
        },
        success:function(data){
            if(data.status){
                var count = thus.parent().children().last().text();
                count = Number(count);
                var temp;
                if(data.message=="add"){
                    temp = count + 1;
                }else{
                    temp = count - 1;
                }
                temp = String(temp);
                thus.parent().children().last().text(temp);
            }else{
                $("#Login-Register-Modal").modal('show');
            }
        },      
        
    });
});

// 收藏功能，点击一次收藏+1，再次点击收藏-1，未登陆不可收藏
$("div.article li span.favorite").click(function () {
    var thus = $(this);
    var title = $(this).parent().parent().parent().parent().children().first().children().first().text();
    $.ajax({
        url:"/favorite/",
        type:"POST",
        dataType:'json',
        data:{
            "title":title,
        },
        success:function(data){
            if(data.status){
                var count = thus.parent().children().last().text();
                count = Number(count);
                var temp;
                if(data.message=="add"){
                    temp = count + 1;
                }else{
                    temp = count - 1;
                }
                temp = String(temp);
                thus.parent().children().last().text(temp);
            }else{
                $("#Login-Register-Modal").modal('show');
            }
        },      
        
    });
});


// 显示评论列表
$("div.article li span.comment").click(function () {
    if($(this).parent().parent().parent().next().hasClass("comment-box")){
        $(this).parent().parent().parent().next().remove();
        return false;
    }
    var thus = $(this);
    var title = $(this).parent().parent().parent().parent().children().first().children().first().text();
    $.ajax({
        url:"/comment/",
        type:"POST",
        dataType:'json',
        data:{
            "title":title,
        },
        success:function(data){
            if(data.status){
                var comment_dict_list = data.message;
                var div_tag = document.createElement("div");
                div_tag.setAttribute("class","comment-box");
                if(comment_dict_list.length == 0){
                    var p_tag = document.createElement("p");
                    p_tag.innerText = "当前没有评论！";
                    p_tag.setAttribute("class", "no-comment");
                    p_tag.style.margin = "10px 10px";
                    div_tag.appendChild(p_tag);
                }else{

                        div_tag.innerHTML=data.message;
                    }
                }
                var target_tag = document.createElement("div");
                var span_tag = document.createElement("span");
                span_tag.innerText= "回复：";
                span_tag.setAttribute("style","color:red");
                target_tag.appendChild(span_tag);
                var target_user_span_tag = document.createElement("span");
                target_user_span_tag.innerText= "";
                target_user_span_tag.setAttribute("style","color:blue");
                target_user_span_tag.setAttribute("id","reply-user");
                target_tag.appendChild(target_user_span_tag);
                var target_comment_span_tag = document.createElement("span");
                target_comment_span_tag.innerText= "";
                target_comment_span_tag.setAttribute("class","hidden");
                target_comment_span_tag.setAttribute("id","reply-comment");
                target_tag.appendChild(target_comment_span_tag);
                var target_time_span_tag = document.createElement("span");
                target_time_span_tag.innerText= "";
                target_time_span_tag.setAttribute("class","hidden");
                target_time_span_tag.setAttribute("id","reply-time");
                target_tag.appendChild(target_time_span_tag);
                div_tag.appendChild(target_tag);

                var input_tag = document.createElement("input");
                input_tag.setAttribute("type","text");
                input_tag.setAttribute("class","col-md-6");
                input_tag.style.margin = "0px 10px";
                input_tag.style.height = "30px";
                div_tag.appendChild(input_tag);

                var button_tag = document.createElement("button");
                button_tag.setAttribute("class","btn btn-primary");
                button_tag.setAttribute("id","make-comment");
                button_tag.style.margin = "0px 10px";
                button_tag.innerText = "评论";
                div_tag.appendChild(button_tag);

                var button_tag_2 = document.createElement("button");
                button_tag_2.setAttribute("class","btn btn-default");
                button_tag_2.setAttribute("id","hangup");
                button_tag_2.innerText = "收起";
                div_tag.appendChild(button_tag_2);

                thus.parent().parent().parent().after(div_tag);

            }
        });
        
    });

$('div.article').delegate("span.reply","click",function () {
    var comment_text = $(this).parent().children().eq(0).text();
    var user = $(this).parent().children().eq(1).text();
    var time = $(this).parent().children().eq(2).text();
    $("#reply-user").text(user);
    $("#reply-comment").text(comment_text);
    $("#reply-time").text(time);
});

// 收起评论按钮动作
$('div.article').delegate("#hangup","click",function(){
    $("div.comment-box").remove();
});

// 发表评论
$('div.article').delegate("#make-comment","click",function(){
    var thus = $(this);
    var show_comment = thus.parent().prev().children().first().children().eq(1).children().first()
    var article = $(this).parent().parent();
    var title = $(this).parent().parent().children().first().children().first().text();
    var comment = $(this).prev().val();
    var father_comment = $("#reply-comment").text();
    var father_user = $("#reply-user").text();
    var father_time = $("#reply-time").text();

    if(comment.length <= 0){
        var error = document.createElement("p");
        error.innerText = "请输入内容...!";
        error.style.color = "red";
        error.style.margin = "0 0 0 10px";
        error.setAttribute("id","make-comment-error-message");
        $(this).prev().before(error);
        window.setTimeout("$('#make-comment-error-message').remove();",1000);
        return false;
    }
    $(this).prev().val("");
    $.ajax({
        url:"/make_comment/",
        type:"POST",
        dataType:'json',
        data:{
            "title":title,
            "comment":comment,
            "father_comment":father_comment,
            "father_user":father_user,
            "father_time":father_time,
        },
        success:function(data){
            if(data.status){
                var count = thus.parent().prev().children().first().children().eq(1).children().last().text();
                count = Number(count) +1;
                thus.parent().prev().children().first().children().eq(1).children().last().text(count);
                $("div.comment-box").remove();
                show_comment.trigger("click");
            }else{
                $("#Login-Register-Modal").modal('show');
            }

        },
    });
});

// 返回顶部按钮
$("div#back_top button").click(function () {
    document.body.scrollTop = 0;
});

function show() {
    var s = document.body.scrollTop;
    var sp = document.getElementById("back_top");
    if(s >=80){
        sp.classList.remove("hide");
    }else{
        sp.classList.add("hide");
    }

}

// 显示回复按钮
$('div.article').delegate("div.comment-line","mouseover",function(over){
    $(this).children().last().removeClass("hidden");
});
// 隐藏回复按钮
$('div.article').delegate("div.comment-line","mouseout",function(over){
    $(this).children().last().addClass("hidden");
});





