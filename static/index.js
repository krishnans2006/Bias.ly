
const randomWords = ["trump", "biden", "senate", "republican", "liberal", "democrat", "congress", "constitution", "senator", "house", "white house", "embassy", "immigrant", "conservative"];

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
        currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}

showDropdown = function (element) {
    var event;
    event = document.createEvent('MouseEvents');
    event.initMouseEvent('mousedown', true, true, window);
    element.dispatchEvent(event);
};

function seehowitworks() {
    const word = randomWords[Math.floor(Math.random() * randomWords.length)];
    let select = document.getElementById("newsselect");
    let selectItems = select.getElementsByTagName("option");
    let selectIndex = Math.floor(Math.random() * selectItems.length);
    let wordpos = 0;
    document.getElementById("searchform").style.border = "6px solid orange";
    document.getElementById("searchform").style.borderRadius = "12px";
    let searchbar = document.getElementById("searchtext");
    searchbar.value = "";
    searchbar.focus();
    let writeToSearch = function() {
        searchbar.value += word[wordpos];
        if (wordpos < word.length - 1) {
            wordpos++;
            setTimeout(function() {writeToSearch()}, 300);
        } else {
            searchbar.value = word;
        }
    }
    writeToSearch();
    setTimeout(function() {select.focus();}, 300 * word.length + 300)
    setTimeout(function() {select.selectedIndex = selectIndex; document.getElementById("queryrun").focus();}, 300 * word.length + 800);
    setTimeout(function() {document.getElementById("searchform").submit();}, 300 * word.length + 1500);
}
