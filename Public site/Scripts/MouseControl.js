onmousemove = function(e){
    document.documentElement.style.setProperty('--x', -e.clientX  + 'px');
    var a = e.clientX / this.window.innerWidth;
    var xPercent = (2 * a)-1;
    document.documentElement.style.setProperty('--xPercent', xPercent);
}