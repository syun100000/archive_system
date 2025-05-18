function get_html_code(id, type) {
    // このコードは、アップロードされたファイルのHTMLの埋め込みコードを返す
    // 用途はレポート記事に添付する際に使う
//     {% if content.type == 'image' %}
//     <div class="content-item">
//         <img src="{{ content.url }}" alt="{{ content.name }}" class="img-fluid">
//         <p class="image-name">{{ content.name }}</p>
//         <a class="btn btn-primary" href="{% url 'upload_contents_detail' content.id %}">コンテンツの詳細</a>
// {% endif %}
// {% if content.type == 'video' %}
//     <div class="content-item">
//         <video src="{{ content.url }}" controls class="video-fluid"></video>
//         <p class="video-name">{{ content.name }}</p>
//         <a class="btn btn-primary" href="{% url 'upload_contents_detail' content.id %}">コンテンツの詳細</a>
//     </div>
// {% endif %}
// {% if content.type == 'youtube' %}
//     <div class="content-item">
//         <iframe src="{{ content.url }}" frameborder="0" allowfullscreen class="youtube-iframe"></iframe>
//         <p class="youtube-title">{{ content.name }}</p>
//         <a class="btn btn-primary" href="{% url 'upload_contents_detail' content.id %}">コンテンツの詳細</a>
//     </div>
// {% endif %}
// {% if content.type == 'audio' %}
//     <div class="content-item">
//         <audio src="{{ content.url }}" controls class="audio-player"></audio>
//         <p class="audio-name">{{ content.name }}</p>
//         <a class="btn btn-primary" href="{% url 'upload_contents_detail' content.id %}">コンテンツの詳細</a>
//     </div>
// {% endif %}
// {% if content.type == 'pdf' %}
//     <div class="content-item">
//         <a href="{{ content.url }}" target="_blank" class="pdf-link">{{ content.name }}</a>
//         <a class="btn btn-primary" href="{% url 'upload_contents_detail' content.id %}">コンテンツの詳細</a>
//     </div>
// {% endif %}
// 上記参考
    // コンテンツの詳細ページのURLを取得
    let upload_contents_detail_url = $(document).find('#upload_contents_detail_url').data('url')
    // アップロードされたファイルのURLを取得　src属性に入れる
    let file_path = $(document).find('#file_path').data('url')
    // ファイル名を取得
    let file_name = $(document).find('#file_name').data('name')
    // ボタンのHTMLを作成
    let button_html = `<a class="btn btn-primary" href="${upload_contents_detail_url}" target="_blank">コンテンツの詳細</a>`
    // 宣言
    let content_html = ''
    let html_code = ''
    // タイプごとにHTMLを作成
    if (type == 'image') {
        content_html = `<img src="${file_path}" alt="${file_name}" class="img-fluid">\
        <p class="image-name">${file_name}</p>`
    }
    else if (type == 'video') {
        content_html = `<video src="${file_path}" controls class="video-fluid"></video>\
        <p class="video-name">${file_name}</p>`
    }
    else if (type == 'youtube') {
        content_html = `<iframe src="${file_path}" frameborder="0" allowfullscreen class="youtube-iframe"></iframe>\
        <p class="youtube-title">${file_name}</p>`
    }
    else if (type == 'audio') {
        content_html = `<audio src="${file_path}" controls class="audio-player"></audio>\
        <p class="audio-name">${file_name}</p>`
    }
    else if (type == 'pdf') {
        content_html = `<a href="${file_path}" target="_blank" class="pdf-link">${file_name}</a>\
        <p class="pdf-name">${file_name}</p>`
    }
    // HTMLコードを作成
    html_code = `<div class="content-item">${content_html}${button_html}</div>`
    console.log(html_code)
    // クリップボードにコピー
    navigator.clipboard.writeText(html_code).then(function() {
        // 成功時の処理
        alert('コピーしました')
    }, function() {
        // 失敗時の処理
        alert('コピーに失敗しました')
    });
    
}