// 現在表示しているモーダルがどの見出しに対するものかを示すグローバル変数
let current_headline = null
// 選択したファイルの情報を保存する連想配列
let selected_files = {};
// selected_filesを見出しごとに保存する配列
let selected_files_by_headline = {};

// 一意の識別子を生成する関数（例：シンプルな連番）
function generateUniqueId() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2);
}
// すでに生成されている見出し1に対してdata-unique-id属性を設定
$('.headline').first().attr('data-unique-id', generateUniqueId());

$('.search-form').on('keyup keypress', function(e) {
    //検索ばーでEnterキーを押したときにページがリロードされるのを防ぐ
    var keyCode = e.keyCode || e.which;
    if (keyCode === 13) { 
      e.preventDefault();
      search_file(e);
      return false;
    }
  });


//見出しフォームのファイル添付ボタンを押したときの処理(モーダルを開く)
$(document).on('click', '.file-select-modal-open-btn', function() {
    // 見出しの識別子を取得
    var uniqueId = $(this).closest('.headline').data('unique-id');
    // モーダルに識別子を設定
    $('#file_select_modal').attr('data-unique-id', uniqueId);
    // 見出しのインデックスを取得しグローバル変数に設定
    current_headline = $(this).data('index');
    // モーダルのタイトルを設定
    $('#fileModalLabel').text("見出し" + current_headline + "のファイル選択");
    // 深いコピーを行う
    selected_files = selected_files_by_headline[uniqueId] ? selected_files_by_headline[uniqueId] : {};
    // selected-file-listに選択したファイルのリストを表示
    $('#selected-file-list-body').empty();
    console.log("selected_files");
    console.log(selected_files);
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
    // 開いてるモーダルの識別子を取得
    var uniqueId = $('#file_select_modal').data('unique-id');
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
            if (response.CODE == 200) {
                // 正常に画像データを受け取った場合
                // ファイルリスト
                for (var i = 0; i < response.FILE_LIST.length; i++) {
                    var file = response.FILE_LIST[i];
                    //ファイルタイプ別の制御
                    if (file.TYPE == 'image') {
                        //画像
                        var selected = is_selected(uniqueId, file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        var img ='<div class="file-item img-thumbnail m-2">\
                                    <img src="' + file.URL + '" alt="画像" class="file-preview" style="width: 100px; height: auto;">\
                                    <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button>\
                                </div>';
                        $('#file-list').append(img);
                    }else if (file.TYPE == 'video') {
                        //動画
                        var selected = is_selected(uniqueId, file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        // var video = '<div class="file-item img-thumbnail m-2">\
                        //                 <video src="' + file.URL + '" class="file-preview" style="width: 100px; height: auto;" controls></video>\
                        //                 <button type="button" class="btn btn-primary file-select-btn" id="file-select-btn' + file.ID + '" onclick="selectfile(\'' + file.ID + '\', \'' + file.URL + '\')">選択</button>\
                        //             </div>';
                        var video = '<div class="file-item img-thumbnail m-2">\
                                        <video src="' + file.URL + '" class="file-preview" style="width: 100px; height: auto;" controls></video>\
                                        <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button>\
                                    </div>';
                        $('#file-list').append(video);
                    }else if (file.TYPE == 'youtube') {
                        //youtube
                        // var youtube = '<div class="file-item img-thumbnail m-2">\
                        //                 <iframe src="' + file.URL + '" class="file-preview" style="width: 100px; height: auto;" frameborder="0" allowfullscreen></iframe>\
                        //                 <button type="button" class="btn btn-primary file-select-btn" id="file-select-btn' + file.ID + '" onclick="selectfile(\'' + file.ID + '\', \'' + file.URL + '\')">選択</button>\
                        //             </div>';
                        var selected = is_selected(uniqueId, file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        var style = `
                        .modal.fade .modal-dialog {
                            -webkit-transition: -webkit-transform 0.3s ease-out;
                                 -moz-transition: -moz-transform 0.3s ease-out;
                                     -o-transition: -o-transform 0.3s ease-out;
                                            transition: transform 0.3s ease-out;
                        }

                        .modal.in .modal-dialog {

                        }
                        `;
                        var youtube = '<div class="file-item img-thumbnail m-2">\
                                            <iframe src="' + file.URL + '" class="file-preview" style="width: 100px; height: auto;" frameborder="0" allowfullscreen></iframe>\
                                            <button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button>\
                                        </div>';
                        $('#file-list').append(youtube);
                    }else if (file.TYPE == 'audio') {
                        //音声
                        if (i == 0) {
                            $('#file-list').append('<p>音声ファイル</p>');
                            var table = '<table class="table table-striped table-bordered table-hover">' +
                                        '<thead><tr><th>ID</th><th>ファイル名</th><th>再生</th><th>選択</th></tr></thead>' +
                                        '<tbody id="audio-list"></tbody></table>';
                            $('#file-list').append(table);
                        }
                        // ファイルが現在の見出しに選択されているかチェックして、ボタンのテキストとクラスを設定
                        var selected = is_selected(uniqueId, file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        // 本番環境ではURLをエンコードする
                        var audio = '<tr><td>' + file.ID + '</td><td>' + file.NAME + '</td><td><audio src="' + file.URL + '" controls></audio></td><td>' +
                            '<button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button></td></tr>';
                        // var audio = '<tr><td>' + file.ID + '</td><td>' + file.NAME + '</td><td><audio src="' + file.URL + '" controls></audio></td><td>' +
                        //     '<button type="button" class="btn btn-primary file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '">選択</button></td></tr>';
                        $('#audio-list').append(audio);
                        
                    }else if (file.TYPE == 'pdf') {
                        //pdf
                        var selected = is_selected(uniqueId, file.ID);
                        var selected_text = selected ? '選択済み' : '選択';
                        var selected_class = selected ? 'btn-secondary selected' : 'btn-primary';
                        if (i == 0) {
                            $('#file-list').append('<p>PDFファイル</p>');
                            var table = '<table class="table table-striped table-bordered table-hover">' +
                                        '<thead><tr><th>ID</th><th>ファイル名</th><th>選択</th></tr></thead>' +
                                        '<tbody id="pdf-list"></tbody></table>';
                            $('#file-list').append(table);
                        }
                        // var pdf = '<tr><td>' + file.ID + '</td><td>' + file.NAME + '</td><td><button type="button" class="btn btn-primary" id="file-select-btn' + file.ID + '" onclick="selectfile(\'' + file.ID + '\', \'' + file.URL + '\',\'' + file.TYPE + '\')">選択</button></td></tr>';
                        var pdf = '<tr><td>' + file.ID + '</td><td>' + file.NAME + '</td><td>' +
                            '<button type="button" class="btn ' + selected_class + ' file-select-btn" data-file-id="' + file.ID + '" data-file-url="' + file.URL + '" data-file-type="' + file.TYPE + '"data-file-name="' + file.NAME + '">' + selected_text + '</button></td></tr>';
                        $('#pdf-list').append(pdf);
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
            alert('検索に失敗しました。');
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
    // ファイルが既に選択されていないか確認
    if (!(file_id in selected_files)) {
        // 選択したファイルの情報を連想配列に保存
        selected_files[file_id] = {name: file_name, url: file_url, type: file_type, id: file_id};
        // ボタンのテキストとクラスを更新
        $(this).text('選択済み').removeClass('btn-primary').addClass('btn-secondary selected');
        // selected_file_listに選択したファイルのリストを表示
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
    else {
        // 選択を解除
        unselectfile(file_id);
    }
});

// select-file-btnを押したときの処理(モーダルを閉じる)
$(document).on('click', '#select-file-btn', function() {
    // 開いてるモーダルの識別子を取得
    var uniqueId = $(this).closest('.modal').data('unique-id');
    // もし選択したファイルがない場合は警告
    if (Object.keys(selected_files).length == 0) {
        alert('ファイルを選択してください。');
        return;
    }
    // 選択したファイルの情報を見出しごとに保存
    selected_files_by_headline[uniqueId] = selected_files;
}
);

// モーダルを閉じたときの共通処理
$('#file_select_modal').on('hidden.bs.modal', function() {
    // 見出しのインデックスをリセット
    current_headline = null;
    // 識別子をリセット
    $(this).removeData('unique-id');
    // 検索結果をリセット
    $('#file-list').empty();
    $('#id_keyword').val('');
    // モーダルのファイルタイプを一番上の選択肢にリセット
    $('#file_type').val($('#file_type option:first').val());
    // 選択したファイル情報のリセット
    selected_files = {};
    console.log(selected_files_by_headline);    
    // selected-file-listのリセット
    $('#selected-file-list-body').empty();
});


// 配列等にファイルIDが含まれているかチェックする関数
function is_selected(uniqueId, file_id) {
    // selected_files_by_headlineに含まれているかチェック
    if (uniqueId in selected_files_by_headline) {
        // 連想配列から含まれているかチェック
        if (file_id in selected_files_by_headline[uniqueId]) {
            return true;
        }
    }
    return false;
}

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

// 識別子がどの見出しのものかを取得する関数
function get_headline_index(uniqueId) {
    return $('[data-unique-id="' + uniqueId + '"]').data('index');
}
















// 見出しの内容の高さを自動調整する
$(document).ready(function() {
    $('.Headline_content').on('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});
$(document).ready(function() {
    // ユーザーが見出しフィールドに入力を行った場合、フラグを設定します。
    $('.headline').on('input', function() {
        isEdited = true;
    });

    // ユーザーがページを離れようとしたとき、フラグが設定されている場合は警告を表示します。
    window.addEventListener('beforeunload', function (e) {
        if (isEdited) {
            e.preventDefault();
            e.returnValue = '';
        }
    });
});
    // フォーム送信時のイベントハンドラ
    $('form').submit(function(e){
        isEdited = false; // フラグをリセット
        var title = $('#title').val().trim();   // タイトルを取得
        var headlineCount = $('.headline').length;  // 見出しの数を取得
        var emptyHeadlines = $('.headline').filter(function() { // 空の見出しを取得
            var headlineInput = $(this).find('.Headline').val().trim();
            var headlineContent = $(this).find('.Headline_content').val().trim();
            return headlineInput === '' && headlineContent === '';
        });
        // タイトルが空の場合に警告
        if(title === '') {
            alert('タイトルを入力してください。');
            e.preventDefault(); // フォームの送信を中止
            return false;
        }
        // 空の見出しがある場合に警告
        if(emptyHeadlines.length > 0) {
            alert('空の見出しがあります。内容を入力するか、削除してください。');
            e.preventDefault(); // フォームの送信を中止
            return false;
        }
        // 見出しが1つのみで、その見出しが空の場合に警告
        if(headlineCount === 1 && emptyHeadlines.length === 1) {
            alert('最低1つの見出しに内容を入力してください。');
            e.preventDefault(); // フォームの送信を中止
            return false;
        }
        // selected_files_by_headlineをJSON文字列に変換して隠しフィールドに設定
        // search_files_by_headlineのキーは一意の識別子なので、そのままでは扱いにくいため、
        // 見出しのインデックスをキーとした連想配列に変換してからJSON文字列に変換
        var selected_files_by_headline_json = {};
        for (var uniqueId in selected_files_by_headline) {
            var index = get_headline_index(uniqueId);
            selected_files_by_headline_json[index] = selected_files_by_headline[uniqueId];
        }
        $('#selected_files_by_headline').val(JSON.stringify(selected_files_by_headline_json));
        // 入力値が正常な場合は送信を続行
        return true;
    });

    // 見出しの数に基づいて削除ボタンの表示を制御する関数
    function controlDeleteButtons() {
        var headlineCount = $('#headline_count').val();
        if(headlineCount == 1){
            $('.del_headline').hide(); // 削除ボタンを非表示にする
        } else {
            $('.del_headline').show(); // 削除ボタンを表示する
        }
    }

    // 見出しを更新する関数
    function updateHeadlines() {
        $('.headline').each(function(index) {
            var newIndex = index + 1;
            $(this).attr('data-index', newIndex);
            $(this).find('label').first().attr('for', 'Headline' + newIndex).text('見出し' + newIndex);
            $(this).find('input').first().attr('id', 'Headline' + newIndex).attr('name', 'Headline' + newIndex).attr('placeholder', '見出し' + newIndex + 'を入力してください');
            $(this).find('textarea').first().attr('id', 'Headline' + newIndex + '_content').attr('name', 'Headline' + newIndex + '_content').attr('placeholder', '見出し' + newIndex + 'の内容を入力してください');
            $(this).find('button').first().attr('data-bs-target', '#file_select_modal').attr('data-headline', 'Headline' + newIndex).attr('data-index', newIndex).text('見出し' + newIndex + 'にファイルを添付');
            $(this).find('.del_headline').first().attr('id', 'del_headline_' + newIndex).text('見出し' + newIndex + 'を削除').show();
            $(this).find('.add_headline_here').first().attr('id', 'add_headline_' + newIndex).text('見出し' + newIndex + 'の下に追加');
        });
        $('#headline_count').val($('.headline').length); // 隠しフィールドを更新
        controlDeleteButtons(); // 削除ボタンの表示を制御
    }

    // 特定の位置に見出しを追加する関数
    function addHeadline(index, $afterElement) {
        var uniqueId = generateUniqueId(); // 一意の識別子を生成
        var add_headline_html = $('<div class="form-group headline" data-index="' + index + '" data-unique-id="' + uniqueId + '"> \
            <label for="Headline' + index + '">見出し' + index + '</label> \
            <input type="text" class="form-control Headline" id="Headline' + index + '" name="Headline' + index + '" placeholder="見出し' + index + 'を入力してください" data-index="' + index + '"> \
            <textarea class="form-control Headline_content" id="Headline' + index + '_content" name="Headline' + index + '_content" rows="3" placeholder="見出し' + index + 'の内容を入力してください" data-index="' + index + '"></textarea> \
            <button type="button" class="btn btn-primary file-select-modal-open-btn" data-bs-toggle="modal" data-bs-target="#file_select_modal" data-headline="Headline' + index + '" data-index="' + index + '"> \
                見出し' + index + 'にファイルを添付 \
            </button> \
            <button type="button" class="btn btn-primary add_headline_here" id="add_headline_'+index+'" data-index="' + index + '">見出し' + index + 'の下に追加</button> \
            <button type="button" class="btn btn-danger del_headline" id="del_headline_'+index+'" data-index="' + index + '">見出し' + index + 'を削除</button> \
        </div>');
        if ($afterElement) {
            $afterElement.after(add_headline_html);
        } else {
            $('#headlines').append(add_headline_html); // 新しい見出しが最後に追加される場合
        }
        selected_files_by_headline[uniqueId] = {}; // selected_files_by_headlineに空の要素を追加
        updateHeadlines();
    }

    // 最下部に見出しを追加するボタンの処理
    $('#add_headline').click(function(){
        var newIndex = $('.headline').length + 1;
        addHeadline(newIndex, null); // 最後の要素の後に追加
    });

    // 特定の位置に見出しを追加するボタンの処理
    $(document).on('click', '.add_headline_here', function(){
        var $currentHeadline = $(this).closest('.headline');
        var position = $currentHeadline.index();
        addHeadline(position + 1, $currentHeadline); // 特定の見出しの後に追加
    });

    // 見出しを削除する関数
    function deleteHeadline(uniqueId) {
        $('[data-unique-id="' + uniqueId + '"]').remove(); // 要素をDOMから削除
        delete selected_files_by_headline[uniqueId]; // 対応するキーを削除
    }
    
    // 見出しを削除するボタンの処理
    $(document).on('click', '.del_headline', function(){
        // どの見出しを削除するかを識別するための一意の識別子を取得
        var uniqueId = $(this).closest('.headline').data('unique-id');
        // 見出しを削除していいか確認
        if (confirm('この見出しを削除しますか？')) {
            deleteHeadline(uniqueId);
            updateHeadlines();
        }
    }
    );



