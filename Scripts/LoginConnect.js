async function VerifyLogin () {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    try{
        login_api(username, password);
    }
    catch (error){
        console.log(error);
    }
}
async function login_api(username, password){
    let res = await fetch("http://127.0.0.1:5000/login", {
        headers: {
            'Accept': 'aplication/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({
            "username": username,
            "password": md5(password)
        })
    });
    let data = await res.json();
    if(data['data'] == 'success'){
        localStorage.setItem('name', username);
        Pass();
    }
    else{
        Deny();
    }
}
function Pass () {
    const passAnimLength=0.5;
    document.getElementById("lock").style.animation="pass " + passAnimLength + "s steps(10)";
    setTimeout(function(){
        window.location.href="/index.html";
        //DONT FORGET TO CHANGE THIS 
    },passAnimLength*999);
}
function Deny () {
    const denyAnimLength = 0.5;
    let lockContainer = document.getElementById("lockContainer");
    
    lockContainer.classList.add("animateDeny");
    setTimeout(function(){
        lockContainer.classList.remove("animateDeny");
    }, denyAnimLength*1000);
}