// このJSはmodalを表示するためのものです。
// モーダルのデフォルトフォームを保持するための変数
let default_form;
// どのボタンが押されたかを判定するための変数
let button;
// data-bs-dismiss='modal'を持つボタンが押された時の動作
$(document).on('click', '[data-bs-dismiss="modal"]', function(){
    console.log('close');
    if (button == 'delete'){
        // アカウント削除が完了した場合はトップページにリダイレクト
        location.href = '/';
    }
    else{
        // ページをリロード
        location.reload();
    }
});
$(document).ready(function() {
    // ページ読み込み完了時にデフォルトフォームを保存
    default_form = $('#modal_form').html();
});
// Email, Name, Passwordの編集ボタンが押された時の処理
function edit_email(){
    button = 'email';
    console.log('edit_email');
    // モーダルのフォームをリセット
    $('#modal_form').html(default_form);
    // モーダルのタイトルを変更
    $('.modal-title').text('メールアドレスの変更');
    // モーダルの説明を変更
    $('.modal-description').text("このフォームに新しいメールアドレスを入力してください。");
    $('.modal-description').append("<br>確認用メールアドレスも入力してください。");
    // モーダルのフォームを変更
    $('#modal_form').append("<div class='mb-3'><label for='email1' class='form-label'>新しいメールアドレス</label><input type='email' name='email1' class='form-control' required></div>");
    // 確認用メールアドレスを追加
    $('#modal_form').append("<div class='mb-3'><label for='email2' class='form-label'>確認用メールアドレス</label><input type='email' name='email2' class='form-control' required></div>");
    // モーダルの送信先を変更
    $('#modal_form').attr('action', '/accounts/edit_email');
    // モーダルを表示
    $('#modal').modal('show');
}
function edit_name(){
    button = 'name';
    console.log('edit_name');
    // モーダルのフォームをリセット
    $('#modal_form').html(default_form);
    // モーダルのタイトルを変更
    $('.modal-title').text('名前の変更');
    // モーダルの説明を変更
    $('.modal-description').text("このフォームに新しい名前を入力してください。");
    // モーダルのフォームを変更
    $('#modal_form').append("<div class='mb-3'><label for='last_name' class='form-label'>新しい姓</label><input type='text' name='last_name' class='form-control' required></div>");
    $('#modal_form').append("<div class='mb-3'><label for='first_name' class='form-label'>新しい名</label><input type='text' name='first_name' class='form-control' required></div>");
    // モーダルの送信先を変更
    $('#modal_form').attr('action', '/accounts/edit_name');
    // モーダルを表示
    $('#modal').modal('show');
}
function edit_password(){
    button = 'password';
    console.log('edit_password');
    // モーダルのフォームをリセット
    $('#modal_form').html(default_form);
    // モーダルのタイトルを変更
    $('.modal-title').text('パスワードの変更');
    // モーダルの説明を変更
    $('.modal-description').text("このフォームに新しいパスワードを入力してください。");
    // モーダルのフォームを変更
    $('#modal_form').append("<div class='mb-3'><label for='password1' class='form-label'>新しいパスワード</label><input type='password' name='password1' class='form-control' required></div>");
    $('#modal_form').append("<div class='mb-3'><label for='password2' class='form-label'>確認用パスワード</label><input type='password' name='password2' class='form-control' required></div>");
    // モーダルの送信先を変更
    $('#modal_form').attr('action', '/accounts/edit_password');
    // モーダルを表示
    $('#modal').modal('show');
}

// アカウント削除ボタンが押された時の処理
function delete_account(){
    console.log('delete_account');
    button = 'delete';
    // モーダルのフォームをリセット
    $('#modal_form').html(default_form);
    // モーダルのタイトルを変更
    $('.modal-title').text('アカウントの削除');
    // モーダルの説明を変更
    $('.modal-description').text("アカウントを削除すると、全てのデータが削除されます。");
    $('.modal-description').append("<br>アカウントを削除してもよろしいですか？");
    // モーダルの送信先を変更
    $('#modal_form').attr('action', '/accounts/delete_account');
    // モーダルを表示
    $('#modal').modal('show');
}
// ajaxでフォームを送信
$(document).on('submit', '#modal_form', function(e){
    e.preventDefault();
    if (button == 'password'){
        // パスワードと確認用パスワードの値を取得
        var password = $('input[name="password1"]').val();
        var confirmPassword = $('input[name="password2"]').val();

        // パスワードが一致しない場合は警告を表示して送信を中止
        if (password !== confirmPassword) {
            alert('パスワードが一致しません。再度入力してください。');
            return;
        }
    }
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function(response){
            console.log(response);
            // バックエンドからコードを受け取り、成功した場合はモーダルの内容を変更
            if (response['code'] == 200){
                console.log('success');
                // 案内メッセージを表示
                if (button == 'email'){
                    $('.modal-body').html("<p>新しいメールアドレスに確認メールを送信しました。</br>メール内のリンクをクリックしてメールアドレスを変更してください。</p>");
                }
                else if (button == 'name'){
                    $('.modal-body').html("<p>名前を変更しました。</p>");
                }
                else if (button == 'password'){
                    $('.modal-body').html("<p>パスワードを変更しました。</p>");
                }
                else if (button == 'delete'){
                    $('.modal-body').html("<p>アカウントを削除しました。</p>");
                    $('.modal-body').append("<p>ご利用ありがとうございました。</p>");
                }
                // モーダルのフッターを閉じるボタンに変更
                $('.modal-footer').html("<button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>閉じる</button>");
            }
            // エラーが発生した場合はエラーメッセージを表示
            else{
                console.log('error', response);
                $('.modal-title').text('エラーが発生しました');
                // エラーメッセージを表示
                $('.modal-body').html("<p>エラーが発生しました。");
                $('.modal-body').append("エラーメッセージ：<br>" + response['error']);
                $('.modal-body').append("<p>エラーが続く場合はお問い合わせください。</p>");
                // モーダルのフッターを閉じるボタンに変更
                $('.modal-footer').html("<button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>閉じる</button>");
            }
        },
        error: function(data){
            console.log(data);
            $('.modal-title').text('エラーが発生しました');
            // エラーメッセージを表示
            $('.modal-body').html("<p>予期せぬエラーが発生しました。</br>もう一度やり直してください。</br>エラーが続く場合はお問い合わせください。</p>");
            // モーダルのフッターを閉じるボタンに変更
            $('.modal-footer').html("<button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>閉じる</button>");
        }
    });
});

