function Scrolled (){
    const element = document.getElementById("contentContainer");
    var c = element.scrollTop / (element.scrollHeight - element.clientHeight);
    var d = c * window.innerWidth;
    document.documentElement.style.setProperty('--scroll', -d  + 'px');
    //collapse this!! This is 1 var at max

}