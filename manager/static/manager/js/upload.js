/**
 * このスクリプトはファイルのアップロード機能の処理を担当します。
 * タイプ選択のドロップダウンの変更を監視し、表示を適切に更新します。
 * 選択された値が1の場合、ファイル入力を表示し、URL入力を非表示にします。
 * 選択された値が2の場合、ファイル入力を非表示にし、URL入力を表示します。
 * また、ファイル入力のラベルを選択されたファイル名で更新します。
 */
$(document).ready(function() {
    $('#type_select').on('change', function() {
        if ($('#type_select').val() == 1) {
            $('#file').css('display', 'block');
            $('#URL').css('display', 'none');
        } else if ($('#type_select').val() == 2) {
            $('#file').css('display', 'none');
            $('#URL').css('display', 'block');
        }
    });
    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });
});