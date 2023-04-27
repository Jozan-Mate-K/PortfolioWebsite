async function fetchHtmlAsText(url) {
    return await (await fetch(url)).text();
}
async function load(whatToLoad) {
    const content = document.getElementById("contentContainer");
    content.scrollTo(0, 0);
    document.title = "Home Project ~ " + whatToLoad.substring(0, whatToLoad.length-5);
    content.innerHTML = await fetchHtmlAsText(whatToLoad);
}