var RegisterHandler = function (){

}

RegisterHandler.prototype.listenSendCaptchaEvent = function (){
    var callback = function (event){
        var $this = $(this);
        //阻止默认的点击事件
        event.preventDefault();
        var email = $("input[name='email']").val();
        var reg =  /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if(!email || !reg.test(email)){
            alert("请输入正确格式的邮箱！");
            return;
        }
        zyajax.get({
            url:"/email/captcha?email="+email,
            success:function (result){
                if(result['code']===200){
                    console.log('邮件发送成功');
                    //取消按钮点击事件
                    $this.off('click');
                    $this.attr("disabled",'disabled');
                    //开始倒计时
                    var countdown =60;
                    var interval=setInterval(function (){
                        if(countdown>0){
                            $this.text(countdown+"s后重新发送");
                        }else {
                            $this.text("发送验证码");
                            $this.attr('disabled',false);
                            $this.on("click",callback);
                            //清理定时器
                            clearInterval(interval);
                        }
                        countdown--;
                    },1000);
                }else{
                    var message = result['message'];
                    alert(message);
                }
            }
        })
    }
    $('#email-captcha-btn').on('click',callback);
}

RegisterHandler.prototype.listenGraphCaptchaEvent=function (){
    //如果运行需要初始化在prototype.run中
    $("#captcha-img").on("click",function (){
        console.log("clicked")
        var $this = $(this);
        var src = $this.attr("src");
        let new_src = zyparam.setParam(src,"sign",Math.random());
        $this.attr("src",new_src);
    });
}

RegisterHandler.prototype.run = function (){
    this.listenSendCaptchaEvent();
    this.listenGraphCaptchaEvent();
}

$(function (){
    var handler = new RegisterHandler();
    handler.run();
})