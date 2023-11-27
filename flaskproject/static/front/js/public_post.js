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
        // uploadImage: {
        // server: '/post/image/upload', // 你的图片上传服务器地址
        // fieldName: 'image', // 你的上传字段名
        // headers: {
        //     "X-CSRFToken": $("meta[name='csrf-token']").attr("content"), // 使用 CSRF token
        //     }
        // }
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

}


PublicPostHandler.prototype.run = function () {
    this.initEditor();

}

$(function(){
    var handler = new PublicPostHandler();
    handler.run();
});