// JQを使用して作成
var generate_count = 0; // 生成回数
// 生成可能なファイルの拡張子
var gpt_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'ico'];
// もしページを離れようとした場合に警告を出す
window.onbeforeunload = function(e) {
    e.returnValue = "本当にページを閉じますか？";
  }
// create-description-btnをクリックした際の処理
// AIによる説明文の作成を行う
$(document).on('click', '#create-description-btn', function() {
    // APIクレジットが減るので，確認を取る
    if (generate_count <1 && !confirm('APIクレジットが減ります．続行しますか？')) {
        return false;
    }
    else if (generate_count >= 1 && !confirm('もう一度生成すると，APIクレジットがさらに減ります．続行しますか？')) {
        return false;
    }
    // 現在のfile_idを取得
    var file_id = $(this).data('file_id');
    // #commentを取得
    var comment = $('#comment').val();
    // もしcommentが空でなければ削除される警告を出す．
    if (comment != '') {
        if (!confirm('AIによる説明文を作成すると，現在の説明文は削除されます．続行しますか？')) {
            return false;
        }
    }
    generate_count += 1;
    $(document).ready(function() {
        // #processing-indicator-descriptionを表示
        $('#processing-indicator-description').show();
    });
    // ajaxでビューのupload_gptにアクセス
    $.ajax({
        url: '/manager/upload_gpt',
        type: 'POST',
        data: {
            'file_id': file_id,
            'action': 'describe',
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        timeout: 60000, // 60秒
        // 成功した場合
        success: function(data) {
            console.log(data);
            if (data.status_code == 200) {
                // #commentにdata.messageを挿入
                $('#comment').val(data.message);
            }
            // ステータスコードがそれ以外の場合
            else {
                // エラーを表示
                alert('エラーが発生しました．エラ-メッセージ：' + data.message);
            }
            $('#processing-indicator-description').hide();
        },
        // 失敗した場合
        error: function(jqXHR, textStatus, errorThrown) {
            $('#processing-indicator-description').hide();
            if (textStatus === 'timeout') {
                alert('リクエストがタイムアウトしました．');
            } else {
                alert('エラーが発生しました．アクセスに失敗しました．');
            }
        }
    });
    // #processing-indicator-descriptionを非表示
});

// create-tags-btnをクリックした際の処理
// AIによるタグの作成を行う
$(document).on('click', '#create-tags-btn', function() {
    // APIクレジットが減るので、確認を取る
    if (generate_count < 1 && !confirm('APIクレジットが減ります。続行しますか？')) {
        return false;
    } else if (generate_count >= 1 && !confirm('もう一度生成すると、APIクレジットがさらに減ります。続行しますか？')) {
        return false;
    }
    
    // 現在のfile_idを取得
    var file_id = $(this).data('file_id');
    
    generate_count += 1;
    
    // #processing-indicator-tagsを表示
    $('#processing-indicator-tags').show();

    // ajaxでビューのupload_gptにアクセス
    $.ajax({
        url: '/manager/upload_gpt',
        type: 'POST',
        data: {
            'file_id': file_id,
            'action': 'tag',
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        timeout: 60000, // 60秒
        // 成功した場合
        success: function(data) {
            console.log(data);
            if (data.status_code == 200) {
                // タグを動的に追加
                var tagsArray = data.tags;  // 例: ["タグ1", "タグ2", "タグ3"]
                // var tagsArray = ["タグ1", "タグ2", "タグ3"]
                tagsArray.forEach(function(tag) {
                    // 既存のタグに重複がない場合のみ追加
                    if (!$('#tags').tagsinput('items').includes(tag)) {
                        $('#tags').tagsinput('add', tag);
                    }
                });
            } else {
                // エラーを表示
                alert('エラーが発生しました。エラーメッセージ：' + data.message);
            }
            $('#processing-indicator-tags').hide();
        },
        // 失敗した場合
        error: function(jqXHR, textStatus, errorThrown) {
            $('#processing-indicator-tags').hide();
            if (textStatus === 'timeout') {
                alert('リクエストがタイムアウトしました。');
            } else {
                alert('エラーが発生しました。アクセスに失敗しました。');
            }
        }
    });
});

// もしファイル拡張子が生成可能なものでなければcreate-description-btnとcreate-tags-btnを非表示にする
$(document).ready(function() {
    var file_extension = $('#file_extension').data('extension');
    console.log(file_extension);
    if (!gpt_extensions.includes(file_extension)) {
        console.log('OK');
        $('#create-description-btn').hide();
        $('#create-tags-btn').hide();
    }
});