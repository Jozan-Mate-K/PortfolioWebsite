function ChangeValue(){
    var rand = 0.875 + (Math.random()/4);
    console.log(rand);
    document.documentElement.style.setProperty('--currentDisplacement', rand);
}
function ScrollToDetails(){
    document.getElementById("detailsSection").scrollIntoView({behavior: "smooth"});
}