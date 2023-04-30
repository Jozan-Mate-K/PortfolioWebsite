function changePassword(){
    let old_pass = document.getElementById("oldPass").value
    let new_pass = document.getElementById("newPass").value
    let conf_new_pass = document.getElementById("confNewPass").value;

    let endpoint = "changepassword";
    let body = {
        'name': localStorage.getItem('name'),
        'old_pass': md5(old_pass),
        'new_pass': md5(new_pass)
    };
    let method = 'POST'
    if(new_pass == conf_new_pass){
        call_api(endpoint, body, method);
    }
    else{
        alert("The passwords don't match");
    }
}

function invite(){
    let endpoint = "invite";
    let body = {
        'name' : document.getElementById("inviteBtn").value
    };
    method = 'POST';
    call_api(endpoint, body, method);
}

async function call_api(endpoint, _body, _method){
    try{

        let res = await fetch("http://127.0.0.1:5000/" + endpoint, {
            headers: {
                'Accept': 'aplication/json',
                'Content-Type': 'application/json'
            },
            method: _method,
            body: JSON.stringify(_body)
        });
        
        let data = await res.json();
    }catch(e){
        console.error(e);
    }
}

function logout(){
    localStorage.clear();
    window.location.href = "/Private";
}

function CheckIfUser(){
    var username = localStorage.getItem('name');
    var token = localStorage.getItem('token');
    if(username == null || token == null){
        logout();
        return;
    }
    let body = {
        'username': username,
        'token': token
    }
    setTimeout(async function(){
        let res = await fetch("http://127.0.0.1:5000/checkToken", {
            headers: {
                'Accept': 'aplication/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(body)
        });
        let data = await res.json();
        if(data['data'] == 'success'){
            return;
        }else{
            logout();
            return;
        }
    }, 100);
    //Here we need to check the sid with the server
}