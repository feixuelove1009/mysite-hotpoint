/**
 * Created by Administrator on 2016/9/5.
 */



$(document).ready(function () {
    $("#login").validate({
        rules : {  //增加rules属性
            username: { required : true , minlength : 4, maxlength:32} ,
            password: { required : true , minlength : 6, maxlength:32} ,
        },

        submitHandler: function(form) {
            var name = $('input[type="text"]').val();
            var pwd = $('input[type="password"]').val();
            $.ajax({
                url:"/login/",
                type:"POST",
                dataType:'json',
                data:{
                    "name":name,
                    "pwd":pwd,
                },
                success:function (data) {
                    if(data.status){
                        $("span.login-message").text("登录成功！返回先前页面...").css({"color":"darkgreen","font-size":"14px"});
                        window.setTimeout("window.location.href='/index/'",1000);
                    }else{
                        $("span.login-message").text(data.message).css({"color":"#ea5d45","font-size":"14px"});
                        window.setTimeout('$("span.login-message").text("").removeAttr("style");',2000);
                    }
                }
            });

         },
        invalidHandler: function(form, validator) {},
    })
});