function Toggle(){
    let form = document.getElementById("emailform");
    if(form.classList.contains("active")){
        form.classList.remove("active");
    }else{
        form.classList.add("active");
    }
}