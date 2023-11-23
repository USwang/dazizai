var SettingHandler = function () {

}
SettingHandler.prototype.listenAvatarUploadEvent = function () {
    $("#avatar-input").on("change",function () {
        var image = this.files[0];
        var formData = new FormData();
        formData.append("image",image);
        zyajax.post({
            url:"/avatar/upload/",
            data:formData,
            processData:false,
            contentType:false,
            success:function (result) {
                // console.log(result);
                if(result['code']===200){
                    var avatar = result['data']['avatar'];
                    var avatar_url = '/media/avatar/'+avatar;
                    // console.log(avatar_url)
                    $("#avatar-img").attr("src",avatar_url)
                }
            }

        })
        // console.log(image);
    });
}

SettingHandler.prototype.listenSubmitEvent = function () {
    $("#submit-btn").on("click",function (event) {
        event.preventDefault();
        var signature = $("#signature-input").val();
        console.log(signature);
        if(!signature){
            signature = "这个人很懒~~";
        }
        // if(signature && (signature.length>50)){
        //     alert("签名长度不应大于50字！");
        //     return;
        // }
        zyajax.post({
            url:"/signature/edit/",
            data:{signature},
            success:function (result) {
                if(result['code']===200){
                    alert("提交成功！")
                    window.location='/'
                }else{
                    alert(result['message'])
                }

            }

        })

    });

}

SettingHandler.prototype.run = function () {
    this.listenAvatarUploadEvent();
    this.listenSubmitEvent();

}

$(function () {
    var handler  = new SettingHandler();
    handler.run();
})