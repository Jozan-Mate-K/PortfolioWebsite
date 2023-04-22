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
    let res = await fetch("http://127.0.0.1:5000/" + endpoint, {
        headers: {
            'Accept': 'aplication/json',
            'Content-Type': 'application/json'
        },
        method: _method,
        body: JSON.stringify(_body)
    });

    let data = await res.json();
    console.log(data);
}

function logout(){
    window.location.href = "/"
}