console.log('mypage.js loaded')

// JQueryを使う
// ID mypage_navを宣言
let mypage_nav 
// はじめに実行
$(document).ready(function() {
    console.log('はじめに実行')
    home_contents()
    // ID mypage_navを取得
    mypage_nav = $('#mypage_nav')
})


function edit_contents() {
    console.log('edit_contents')
    // ID mypage_homeのコンテンツを非表示にする
    $('#home_contents').hide()
    // ID edit_contentsのコンテンツを表示する
    $('#edit_contents').show()
    // ID edit_contents_buttonのclassをactiveにする
    $('#edit_contents_button').addClass('active');
    // ID home_contents_buttonのclassをactiveから削除する
    $('#home_contents_button').removeClass('active');
}

function home_contents() {
    console.log('mypage_home')
    // ID edit_contentsのコンテンツを非表示にする
    $('#edit_contents').hide()
    // ID home_contentsのコンテンツを表示する
    $('#home_contents').show()
    // ID home_contents_buttonのclassをactiveにする
    $('#home_contents_button').addClass('active');
    // ID edit_contents_buttonのclassをactiveから削除する
    $('#edit_contents_button').removeClass('active');
}