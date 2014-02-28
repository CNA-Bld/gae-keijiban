var dom = function (id) { return document.getElementById(id); }

var content = dom("content");
var faceList = ["|∀ﾟ", "(´ﾟДﾟ`)", "(;´Д`)", "(｀･ω･)", "(=ﾟωﾟ)=", "| ω・´)", "|-` )", "|д` )", "|ー` )", "|∀` )", "(つд⊂)", "(ﾟДﾟ≡ﾟДﾟ)", "(＾o＾)ﾉ", "(|||ﾟДﾟ)", "( ﾟ∀ﾟ)", "( ´∀`)", "(*´∀`)", "(*ﾟ∇ﾟ)", "(*ﾟーﾟ)", "(　ﾟ 3ﾟ)", "( ´ー`)", "( ・_ゝ・)", "( ´_ゝ`)", "(*´д`)", "(・ー・)", "(・∀・)", "(ゝ∀･)", "(〃∀〃)", "(*ﾟ∀ﾟ*)", "( ﾟ∀。)", "( `д´)", "(`ε´ )", "(`ヮ´ )", "σ`∀´)", " ﾟ∀ﾟ)σ", "ﾟ ∀ﾟ)ノ", "(╬ﾟдﾟ)", "(|||ﾟдﾟ)", "( ﾟдﾟ)", "Σ( ﾟдﾟ)", "( ;ﾟдﾟ)", "( ;´д`)", "(　д ) ﾟ ﾟ", "( ☉д⊙)", "(((　ﾟдﾟ)))", "( ` ・´)", "( ´д`)", "( -д-)", "(>д<)", "･ﾟ( ﾉд`ﾟ)", "( TдT)", "(￣∇￣)", "(￣3￣)", "(￣ｰ￣)", "(￣ . ￣)", "(￣皿￣)", "(￣艸￣)", "(￣︿￣)", "(￣︶￣)", "ヾ(´ωﾟ｀)", "(*´ω`*)", "(・ω・)", "( ´・ω)", "(｀・ω)", "(´・ω・`)", "(`・ω・´)", "( `_っ´)", "( `ー´)", "( ´_っ`)", "( ´ρ`)", "( ﾟωﾟ)", "(oﾟωﾟo)", "(　^ω^)", "(｡◕∀◕｡)", "/( ◕‿‿◕ )\\", "ヾ(´ε`ヾ)", "(ノﾟ∀ﾟ)ノ", "(σﾟдﾟ)σ", "(σﾟ∀ﾟ)σ", "|дﾟ )", "┃電柱┃", "ﾟ(つд`ﾟ)", "ﾟÅﾟ )　", "⊂彡☆))д`)", "⊂彡☆))д´)", "⊂彡☆))∀`)", "(´∀((☆ミつ"];
var optionsList = dom("emotion").options;
for (var i = 0; i < faceList.length; i++) {
    optionsList[1 + i] = new Option(faceList[i], faceList[i]);
}
dom("emotion").onchange = function (i) { if (this.selectedIndex != 0) { content.value += this.value; var l = content.value.length; content.focus(); content.setSelectionRange(l, l); } }
content.onkeydown = function (e) {
    return (check() || e.keyCode == 8);
}
function check() {
    if (content.value.length > 500) {
        dom("max").style.display = "";
        return false;
    }
    else {
        dom("max").style.display = "none";
        return true;
    }
}
var a = document.getElementsByTagName("a");
for (var i = 0; i < a.length; i++) {
    if (a[i].className == "r") a[i].onclick = function () {
        addRef(this.rel);
    }
}
function addRef(id) {
    content.value += ">>No." + id + "\r\n"; content.scrollTop = content.scrollHeight;
}
function isIE() {
    return /MSIE 6\.0/i.test(navigator.userAgent) || /MSIE 7\.0/i.test(navigator.userAgent);
}
