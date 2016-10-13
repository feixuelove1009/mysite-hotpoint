/**
 * Created by Administrator on 2016/9/5.
 */

$(document).ready(function () {

    $("#register input[type='reset']").click(function () {
        $("#register label.error").remove();
    });


    $("#register").validate({
        rules : {  //增加rules属性
            username: { required : true , minlength : 4, maxlength:32} ,
            password: { required : true , minlength : 6, maxlength:32} ,
            password_confirm: { required : true , minlength : 6, maxlength:32, equalTo:"#Password1"} ,
            email : { required : true , email : true} ,
        },
        submitHandler: function(form) {                
                var name = $('#register input[type="text"]').val();
                var pwd = $('#register input[name="password"]').val();
                var pwd_confirm = $('#register input[name="password_confirm"]').val();
                var email = $('#register input[type="email"]').val();
                $.ajax({
                    url:"/register/",
                    type:"POST",
                    dataType:'json',
                    data:{
                        "name":name,
                        "pwd":pwd,
                        "pwd_confirm":pwd_confirm,
                        "email":email,
                    },
                    success:function (data) {
                        if(data.status){
                            $("span.register-message").text("注册成功！返回先前页面...").css({"color":"darkgreen","font-size":"14px"})
                            window.setTimeout("window.location.href='/index/'",1000);
                        }else{
                            $("span.register-message").text(data.message).css({"color":"#ea5d45","font-size":"14px"})
                            window.setTimeout('$("span.register-message").text("").removeAttr("style");',2000);
                        }
                    }
                });
        },
        invalidHandler: function(form, validator) {}
    })
});

