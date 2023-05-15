function Scrolled (){
    const element = document.getElementById("contentContainer");
    var c = element.scrollTop / (element.scrollHeight - element.clientHeight);
    var d = c * window.innerWidth;
    document.documentElement.style.setProperty('--scroll', -d  + 'px');
}
function Reveal (){
    var reveals = document.querySelectorAll('.reveal');
    for (let i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var revealTop = reveals[i].getBoundingClientRect().top;
        var revealBottom = reveals[i].getBoundingClientRect().bottom;
        var revealPoint = 200;



        if(revealTop < windowHeight - revealPoint){
            reveals[i].classList.add("active");
        }else{
            reveals[i].classList.remove("active");
        } 
        if(revealBottom < revealPoint){
            reveals[i].classList.remove("active");
        }
    }
}
onmousemove = function(e){
    document.documentElement.style.setProperty('--x', -e.clientX  + 'px');
    var a = e.clientX / this.window.innerWidth;
    var xPercent = (2 * a)-1;
    document.documentElement.style.setProperty('--xPercent', xPercent);
}