var PublicPostHandler = function () {

}

PublicPostHandler.prototype.initEditor = function () {
    // var E = window.wangEditor;
    var csrf_token=$("meta[name='csrf-token']").attr("content");
    const { createEditor, createToolbar } = window.wangEditor;

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
          const html = editor.getHtml()
          console.log('editor content', html)
          // 也可以同步到 <textarea>
        },
        MENU_CONF:{},
    };
    editorConfig.MENU_CONF['uploadImage'] = {
     server: '/post/image/upload',
     fieldName: 'image',
     headers: {
        "X-CSRFToken": csrf_token
        },
    };
    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    });

    const toolbarConfig = {};

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    });
    this.editor =editor;
}


PublicPostHandler.prototype.listenSubmitEvent = function () {
    var that = this;
    $("#submit-btn").on("click",function (event) {
        event.preventDefault();
        var title = $("input[name='title']").val();
        var board_id = $("select[name='board_id']").val();
        var content = that.editor.getHtml() ;
        zyajax.post({
            url:"/post/public",
            data:{title,board_id,content},
            success:function (result) {
                if(result['code']===200){
                    let data = result['data'];
                    let post_id = data['id'];
                    window.location = "/post/detail/" + post_id;
                }else {
                    alert(result['message'])
                }

            }
        });

    });

}

PublicPostHandler.prototype.run = function () {
    this.initEditor();
    this.listenSubmitEvent();

}

$(function(){
    var handler = new PublicPostHandler();
    handler.run();
});