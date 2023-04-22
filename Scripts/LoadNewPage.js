async function fetchHtmlAsText(url) {
    return await (await fetch(url)).text();
}
async function load(whatToLoad) {
    const content = document.getElementById("contentContainer");
    content.innerHTML = await fetchHtmlAsText(whatToLoad);
}