// ファイル選択モーダルのスクリプト
let selected_files = {}; // 選択したファイルの情報を保存する連想配列
let toggle_url_output = false; // URL出力を選択しているかどうかのフラグ true: ファイルのURLを出力 false: アーカイブコンテンツ詳細ページのURLを出力
// トグルスイッチの変更イベントを監視
$(document).on('change', '#toggle-url-output', function() {
    if ($(this).is(':checked')) {
        toggle_url_output = true;
    }
    else {
        toggle_url_output = false;
    }
});

//見出しフォームのファイル添付ボタンを押したときの処理(モーダルを開く)
$(document).on('click', '.file-select-modal-open-btn', function() {
    console.log("file-select-modal-open-btn");
    $('#file_select_modal').modal('show');
    // モーダルのタイトルを設定
    $('#fileModalLabel').text("ファイル選択");
    // selected-file-listに選択したファイルのリストを表示
    $('#selected-file-list-body').empty();
    for (var file_id in selected_files) {
        var file = selected_files[file_id];
        var file_type = file.type;
        var file_name = file.name;
        var file_url = file.url;
        var file_item = '<tr>\
                            <td>' + file_id + '</td>\
                            <td><a href="' + file_url + '" target="_blank">' + file_name + '</a></td>\
                            <td>' + file_type + '</td>\
                            <td>\
                                <button type="button" class="btn btn-danger file-select-btn selected" data-file-id="' + file_id + '" data-file-url="' + file_url + '" data-file-type="' + file_type + '"data-file-name="' + file_name + '">選択済み</button>\
                            </td>\
                        </tr>';
        $('#selected-file-list-body').append(file_item);
    }
});
// サーバーからファイルを取得する関数
function search_file(event) {
    event.preventDefault();
    if ($('#id_keyword').val() == '') {
        alert('検索キーワードを入力してください。');
        return;
    }
    if ($('#file_type').val() == '') {
        alert('ファイルタイプを選択してください。');
        return;
    }
    var keyword = $('#id_keyword').val();
    var file_type = $('#file_type').val();
    // テンプレートのdata-url属性からajaxのurlを取得
    var url = $("#search_file_url").data("url");
    // トークンを取得
    var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
    var data = {
        'keyword': keyword,
        'file_type': file_type,
        'csrfmiddlewaretoken': csrfmiddlewaretoken
    };
    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function(response) {
            // サーバーからの応答をそのまま使用
            $('#file-list').empty();
            $('#file-list').append('<table class="table table-striped table-bordered table-hover style="width: 100%;">\
                                        <thead>\
                                            <tr>\
                                                <th>ID</th>\
                                                <th>タイトル</th>\
                                                <th>ファイル名</th>\
                                                <th>詳細</th>\
                                                <th>選択</th>\
                                            </tr>\
                                        </thead>\
                                        <tbody id="file-list-body"></tbody>\
                                    </table>');
            if (response.CODE == 200) {
                // 正常に画像データを受け取った場合
                // ファイルリスト
                for (var i = 0; i < response.FILE_LIST.length; i++) {
                    var file = response.FILE_LIST[i];
                    console.log(file);
                    //ファイルタイプ別の制御
                    if (file.TYPE == 'image') {
                        //画像
                        var selected = is_selected(file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        // var img ='<div class="file-item img-thumbnail m-2">\
                        //             <img src="' + file.URL + '" alt="画像" class="file-preview" style="width: 100px; height: auto;">\
                        //             <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button>\
                        //         </div>';
                        // $('#file-list').append(img);
                        var img = '<tr>\
                                    <td>' + file.ID + '</td>\
                                    <td>' + file.TITLE + '</td>\
                                    <td><img src="' + file.URL + '" alt="画像" style="width: 100px; height: auto;">\
                                    <p>' + file.NAME + '</p></td>\
                                    <td><a href="/upload_contents_detail/' + file.ID + '" target="_blank">詳細</a></td>\
                                    <td>\
                                        <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '" data-file-name="' + file.NAME + '" data-file-title="' + file.TITLE + '">' + selected_text + '</button>\
                                    </td>\
                                </tr>';
                        $('#file-list-body').append(img);
                    }else if (file.TYPE == 'video') {
                        //動画
                        var selected = is_selected(file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        // var video = '<div class="file-item img-thumbnail m-2">\
                        //                 <video src="' + file.URL + '" class="file-preview" style="width: 100px; height: auto;" controls></video>\
                        //                 <button type="button" class="btn btn-primary file-select-btn" id="file-select-btn' + file.ID + '" onclick="selectfile(\'' + file.ID + '\', \'' + file.URL + '\')">選択</button>\
                        //             </div>';
                        // var video = '<div class="file-item img-thumbnail m-2">\
                        //                 <video src="' + file.URL + '" class="file-preview" style="width: 100px; height: auto;" controls></video>\
                        //                 <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button>\
                        //             </div>';
                        // $('#file-list').append(video);
                        var video = '<tr>\
                                    <td>' + file.ID + '</td>\
                                    <td>' + file.TITLE + '</td>\
                                    <td><video src="' + file.URL + '" style="width: 100px; height: auto;" controls></video>\
                                    <p>' + file.NAME + '</p></td>\
                                    <td><a href="/upload_contents_detail/' + file.ID + '" target="_blank">詳細</a></td>\
                                    <td>\
                                        <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '" data-file-name="' + file.NAME + '" data-file-title="' + file.TITLE + '">' + selected_text + '</button>\
                                    </td>\
                                </tr>';
                        $('#file-list-body').append(video);
                    }else if (file.TYPE == 'youtube') {
                        //youtube
                        // var youtube = '<div class="file-item img-thumbnail m-2">\
                        //                 <iframe src="' + file.URL + '" class="file-preview" style="width: 100px; height: auto;" frameborder="0" allowfullscreen></iframe>\
                        //                 <button type="button" class="btn btn-primary file-select-btn" id="file-select-btn' + file.ID + '" onclick="selectfile(\'' + file.ID + '\', \'' + file.URL + '\')">選択</button>\
                        //             </div>';
                        var selected = is_selected(file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        // var style = `
                        // .modal.fade .modal-dialog {
                        //     -webkit-transition: -webkit-transform 0.3s ease-out;
                        //          -moz-transition: -moz-transform 0.3s ease-out;
                        //              -o-transition: -o-transform 0.3s ease-out;
                        //                     transition: transform 0.3s ease-out;
                        // }

                        // .modal.in .modal-dialog {

                        // }
                        // `;
                        // var youtube = '<div class="file-item img-thumbnail m-2">\
                        //                     <iframe src="' + file.URL + '" class="file-preview" style="width: 100px; height: auto;" frameborder="0" allowfullscreen></iframe>\
                        //                     <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button>\
                        //                 </div>';
                        // $('#file-list').append(youtube);
                        var youtube = '<tr>\
                                    <td>' + file.ID + '</td>\
                                    <td>' + file.TITLE + '</td>\
                                    <td><iframe src="' + file.URL + '" style="width: 100px; height: auto;" frameborder="0" allowfullscreen></iframe>\
                                    <p>' + file.NAME + '</p></td>\
                                    <td><a href="/upload_contents_detail/' + file.ID + '" target="_blank">詳細</a></td>\
                                    <td>\
                                        <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '" data-file-name="' + file.NAME + '" data-file-title="' + file.TITLE + '">' + selected_text + '</button>\
                                    </td>\
                                </tr>';
                        $('#file-list-body').append(youtube);
                    }else if (file.TYPE == 'audio') {
                        //音声
                        // if (i == 0) {
                        //     $('#file-list').append('<p>音声ファイル</p>');
                        //     var table = '<table class="table table-striped table-bordered table-hover">' +
                        //                 '<thead><tr><th>ID</th><th>ファイル名</th><th>再生</th><th>選択</th></tr></thead>' +
                        //                 '<tbody id="audio-list"></tbody></table>';
                        //     $('#file-list').append(table);
                        // }
                        // ファイルが現在の見出しに選択されているかチェックして、ボタンのテキストとクラスを設定
                        var selected = is_selected(file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        // var audio = '<tr><td>' + file.ID + '</td><td>' + file.NAME + '</td><td><audio src="' + file.URL + '" controls></audio></td><td>' +
                        //     '<button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button></td></tr>';
                        // $('#audio-list').append(audio);
                        var audio = '<tr>\
                                    <td>' + file.ID + '</td>\
                                    <td>' + file.TITLE + '</td>\
                                    <td><audio src="' + file.URL + '" controls></audio>\
                                    <p>' + file.NAME + '</p></td>\
                                    <td><a href="/upload_contents_detail/' + file.ID + '" target="_blank">詳細</a></td>\
                                    <td>\
                                        <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '" data-file-name="' + file.NAME + '" data-file-title="' + file.TITLE + '">' + selected_text + '</button>\
                                    </td>\
                                </tr>';
                        $('#file-list-body').append(audio);;
                        
                    }else if (file.TYPE == 'pdf') {
                        //pdf
                        var selected = is_selected(file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        // if (i == 0) {
                        //     $('#file-list').append('<p>PDFファイル</p>');
                        //     var table = '<table class="table table-striped table-bordered table-hover">' +
                        //                 '<thead><tr><th>ID</th><th>ファイル名</th><th>選択</th></tr></thead>' +
                        //                 '<tbody id="pdf-list"></tbody></table>';
                        //     $('#file-list').append(table);
                        // }
                        // // var pdf = '<tr><td>' + file.ID + '</td><td>' + file.NAME + '</td><td><button type="button" class="btn btn-primary" id="file-select-btn' + file.ID + '" onclick="selectfile(\'' + file.ID + '\', \'' + file.URL + '\',\'' + file.TYPE + '\')">選択</button></td></tr>';
                        // var pdf = '<tr><td>' + file.ID + '</td><td>' + file.NAME + '</td><td>' +
                        //     '<button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button></td></tr>';
                        // $('#pdf-list').append(pdf);
                        var pdf = '<tr>\
                                    <td>' + file.ID + '</td>\
                                    <td>' + file.TITLE + '</td>\
                                    <td><a href="' + file.URL + '" target="_blank">PDFファイルを開く</a>\
                                    <p>' + file.NAME + '</p></td>\
                                    <td><a href="/upload_contents_detail/' + file.ID + '" target="_blank">詳細</a></td>\
                                    <td>\
                                        <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '" data-file-name="' + file.NAME + '" data-file-title="' + file.TITLE + '">' + selected_text + '</button>\
                                    </td>\
                                </tr>';
                        $('#file-list-body').append(pdf);
                    }
                }
            } else if (response.CODE == 404) {
                // 検索結果が0件の場合
                $('#file-list').append('<p>検索結果が見つかりませんでした。</p>');
            } else if (response.CODE == 413) {
                // 検索結果が100件を超えた場合
                $('#file-list').append('<p>検索結果が100件を超えました。検索条件を変更してください。</p>');
            } else {
                // その他のエラー
                $('#file-list').append('<p>不明なエラーが発生しました。<br>\
                サーバーからの応答がありません。しばらく待ってから再度お試しください。<br>\
                改善しない場合は管理者にお問い合わせください。</p>');
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert('検索に失敗しました。ajax通信に失敗しました。');
            $('#file-list').empty();
            $('#file-list').append('<p>不明なエラーが発生しました。<br>\
            サーバーからの応答がありません。しばらく待ってから再度お試しください。<br>\
            改善しない場合は管理者にお問い合わせください。</p>');
        }
    }
    );
    }

// 選択ボタンを押したときの処理
$(document).on('click', '.file-select-btn', function() {
    var file_id = $(this).data('file-id');
    var file_name = $(this).data('file-name');
    var file_url = $(this).data('file-url');
    var file_type = $(this).data('file-type');
    var file_title = $(this).data('file-title');
    // ファイルが既に選択されていないか確認
    if (!(file_id in selected_files)) {
        // 選択したファイルの情報を連想配列に保存
        selected_files[file_id] = {name: file_name, url: file_url, type: file_type, id: file_id};
        // ボタンのテキストとクラスを更新
        $(this).text('選択済み').removeClass('btn-primary').addClass('btn-secondary selected');
        // selected_file_listに選択したファイルのリストを表示
        // var file_item = '<tr>\
        //                     <td>' + file_id + '</td>\
        //                     <td><a href="' + file_url + '" target="_blank">' + file_name + '</a></td>\
        //                     <td>' + file_type + '</td>\
        //                     <td>\
        //                         <button type="button" class="btn btn-danger file-select-btn selected" data-file-id="' + file_id + '" data-file-url="' + file_url + '" data-file-type="' + file_type + '"data-file-name="' + file_name + '">選択済み</button>\
        //                     </td>\
        //                 </tr>';
        var file_item = '<tr>\
                            <td>' + file_id + '</td>\
                            <td>' + file_title + '</td>\
                            <td>' + file_name + '</td>\
                            <td>' + file_type + '</td>\
                            <td>\
                                <button type="button" class="btn btn-danger file-select-btn selected" data-file-id="' + file_id + '" data-file-url="' + file_url + '" data-file-type="' + file_type + '"data-file-name="' + file_name + '">選択済み</button>\
                            </td>\
                        </tr>';
        $('#selected-file-list-body').append(file_item);
    }
    else {
        // 選択を解除
        unselectfile(file_id);
    }
});

// 　選択を解除するときの共通処理関数
function unselectfile(file_id) {
    // selected_filesに含まれているかチェック
    if (file_id in selected_files) {
        // 連想配列から削除
        delete selected_files[file_id];
        // ボタンのテキストとクラスを更新
        $('.file-select-btn[data-file-id="' + file_id + '"]').text('選択').removeClass('btn-secondary selected').addClass('btn-primary');
    }
    // selected_file_listから削除
    $('#selected-file-list-body').find('button[data-file-id="' + file_id + '"]').closest('tr').remove();
}

// file-select-btn　selected　を押したときの処理
$(document).on('click', '.selected', function() {
    var file_id = $(this).data('file-id');
    unselectfile(file_id);
});
// select-file-btnを押したときの処理(モーダルを閉じてコンテンツを挿入)
$(document).on('click', '#select-file-btn', function() {
    // もし選択したファイルがない場合は警告
    if (Object.keys(selected_files).length == 0) {
        alert('ファイルを選択してください。');
        return;
    }
    const editor = window.editors["editor"]; // キーを一致させる
    if (editor) {
        console.log("editor");
        editor.model.change(writer => {
            const insertPosition = editor.model.document.selection.getFirstPosition();
            for (let file_id in selected_files) {
                const file = selected_files[file_id];
                if (toggle_url_output) {
                    console.log("toggle_url_output");
                    // URL出力を選択している場合 ファイルのURLを挿入
                    const html = generate_file_url(file.id, file.url, file.type);
                    const viewFragment = editor.data.processor.toView(html);
                    const modelFragment = editor.data.toModel(viewFragment);
                    writer.insert(modelFragment, insertPosition);
                } else {
                    console.log("toggle_url_output false");
                    // URL出力を選択していない場合 アーカイブコンテンツのURLを挿入
                    const html = generate_file_upload(file.id, file.url, file.type);
                    const viewFragment = editor.data.processor.toView(html);
                    const modelFragment = editor.data.toModel(viewFragment);
                    writer.insert(modelFragment, insertPosition);
                }
            }
        });
        // モーダルを閉じる
        $('#file-list').empty();
        $('#id_keyword').val('');
        // モーダルのファイルタイプを一番上の選択肢にリセット
        $('#file_type').val($('#file_type option:first').val());
        // 選択したファイル情報のリセット
        selected_files = {}; 
        // selected-file-listのリセット
        $('#selected-file-list-body').empty();
    } else {
        console.error('エディターインスタンスが見つかりません。');
    }

}
);

// モーダルを閉じたときの共通処理 おそらく使われていない
$('#file_select_modal').on('hidden.bs.modal', function() {
    console.log("file_select_modal hidden.bs.modal");
    // 検索結果をリセット
    $('#file-list').empty();
    $('#id_keyword').val('');
    // モーダルのファイルタイプを一番上の選択肢にリセット
    $('#file_type').val($('#file_type option:first').val());
    // 選択したファイル情報のリセット
    selected_files = {}; 
    // selected-file-listのリセット
    $('#selected-file-list-body').empty();
});


// 配列等にファイルIDが含まれているかチェックする関数
function is_selected(file_id) {
    if (file_id in selected_files) {
        return true;
    }
    return false;
}

// 挿入用ファイルのHTMLを生成する関数（コンテンツファイルを直接挿入する）
function generate_file_url(file_id, file_url, file_type) {
    var html = '';
    if (file_type == 'image') {
        html = '<img src="' + file_url + '" alt="画像" style="width: 100%; height: auto;">';
    } else if (file_type == 'video') {
        html = '<video src="' + file_url + '" style="width: 100%; height: auto;" controls></video>';
    } else if (file_type == 'youtube') {
        html = '<iframe src="' + file_url + '" style="width: 100%; height: auto;" frameborder="0" allowfullscreen></iframe>';
    } else if (file_type == 'audio') {
        html = '<audio src="' + file_url + '" controls></audio>';
    } else if (file_type == 'pdf') {
        html = '<a href="' + file_url + '" target="_blank">PDFファイルを開く</a>';
    }
    return html;
}

// 挿入用ファイルのHTMLを生成する関数（アーカイブコンテンツのURLを挿入する）
function generate_file_upload(file_id, file_url, file_type) {
    var upload_url = "/upload_contents_detail/" + file_id + "/";
    var html = '';
    if (file_type == 'image') {
        html = '<div style="display: flex; flex-direction: column; align-items: center;">';
        html += '<img src="' + file_url + '" alt="画像" style="width: 100%; height: auto;">';
        html += '<a href="' + upload_url + '" target="_blank" class="btn btn-primary" style="margin-top: 10px;">アーカイブコンテンツを開く</a>';
        html += '</div>';
        } else if (file_type == 'video') {
        html = '<div style="display: flex; flex-direction: column; align-items: center;">';
        html += '<video src="' + file_url + '" style="width: 100%; height: auto;" controls></video>';
        html += '<a href="' + upload_url + '" target="_blank" class="btn btn-primary" style="margin-top: 10px;">アーカイブコンテンツを開く</a>';
        html += '</div>';
        } else if (file_type == 'youtube') {
        html = '<div style="display: flex; flex-direction: column; align-items: center;">';
        html += '<iframe src="' + file_url + '" style="width: 100%; height: auto;" frameborder="0" allowfullscreen></iframe>';
        html += '<a href="' + upload_url + '" target="_blank" class="btn btn-primary" style="margin-top: 10px;">アーカイブコンテンツを開く</a>';
        html += '</div>';
        } else if (file_type == 'audio') {
        html = '<div style="display: flex; flex-direction: column; align-items: center;">';
        html += '<audio src="' + file_url + '" controls></audio>';
        html += '<a href="' + upload_url + '" target="_blank" class="btn btn-primary" style="margin-top: 10px;">アーカイブコンテンツを開く</a>';
        html += '</div>';
    }
    else if (file_type == 'pdf') {
        html = '<a href="' + upload_url + '" target="_blank" class="btn btn-primary">アーカイブコンテンツを開く</a>';
    }
    return html;
}