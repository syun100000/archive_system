// クッキー保存関数
function setCookie(cname, cvalue, exminutes) {
  var d = new Date();
  d.setTime(d.getTime() + (exminutes * 60 * 1000));
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// クッキー取得関数
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var cookies = decodedCookie.split(';');
  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i];
    while (cookie.charAt(0) === ' ') {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return "";
}

function toggleFontSize() {
  var currentState = getCookie("fontSizeState");
  var paragraphs = document.querySelectorAll('p,a,table');
  var headings = document.querySelectorAll('h1, h2, h3');
  var fontSizeButton = document.getElementById("fontSizeButton");

  if (currentState === "large") {
    for (var i = 0; i < paragraphs.length; i++) {
      paragraphs[i].style.fontSize = ""; // 標準のフォントサイズに戻す
    }
    for (var j = 0; j < headings.length; j++) {
      headings[j].style.fontSize = ""; // 標準のフォントサイズに戻す
    }
    setCookie("fontSizeState", "normal", 5); // 5分間有効なクッキーをセットする
    fontSizeButton.textContent = "文字を拡大する"; // ボタンのテキストを変更
  } else {
    for (var i = 0; i < paragraphs.length; i++) {
      var currentSize = parseInt(window.getComputedStyle(paragraphs[i]).fontSize);
      var newSize = currentSize + 8; // 5pxずつ拡大する例
      paragraphs[i].style.fontSize = newSize + 'px';
    }
    for (var j = 0; j < headings.length; j++) {
      var currentSize = parseInt(window.getComputedStyle(headings[j]).fontSize);
      var newSize = currentSize + 8; // 5pxずつ拡大する例
      headings[j].style.fontSize = newSize + 'px';
    }
    setCookie("fontSizeState", "large", 5); // 5分間有効なクッキーをセットする
    fontSizeButton.textContent = "文字を縮小する"; // ボタンのテキストを変更
  }
}
// ページ読み込み時に実行する処理
window.onload = function() {
  var currentState = getCookie("fontSizeState");
  if (currentState === "large") {
    toggleFontSize(); // ページ読み込み時に拡大状態を復元
  }
}