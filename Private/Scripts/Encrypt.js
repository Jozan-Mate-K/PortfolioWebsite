const backendIp = "https://jmbackend.eu-north-1.elasticbeanstalk.com"; 

function MD5_hash(){
    document.getElementById('hashed_md5').value = md5(document.getElementById('plain_text_md5').value);
};

function AES(){
    if (document.getElementById("aes_plain_text").value.length < 1){
        AES_dec();
    }
    else{
        AES_enc();
    }
}

function AES_enc(){
    var text = document.getElementById("aes_plain_text").value;
    var key = document.getElementById("aes_key").value;

    aes_api(text, key, 'enc');   
}

function AES_dec(){
    var text = document.getElementById("aes_cypher_text").value;
    var key = document.getElementById("aes_key").value;

    aes_api(text, key, 'dec');
}

async function aes_api(text, key, type){
    
    let res = await fetch(backendIp + "/aes", {
        headers: {
            'Accept': 'aplication/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({
            'text': text,
            'key': key,
            'type' : type
    })});
    let data = await res.json();

    if(type == 'enc'){
        document.getElementById("aes_cypher_text").value = data['data'];
        document.getElementById("aes_plain_text").value = ""
    }
    else{
        document.getElementById("aes_plain_text").value = data['data']
        document.getElementById("aes_cypher_text").value = ""
    }
    
}
function SHA256(){
    if (document.getElementById("rsa_plain_text").value.length < 1){
        SHA256_dec();
    }
    else{
        SHA256_enc();
    }
}
function SHA256_enc(){
    let text = document.getElementById("rsa_plain_text").value;
    let key = document.getElementById("rsa_pub_key").value;

    sha_api(text, key, 'enc');
}
function SHA256_dec(){
    let text = document.getElementById("rsa_cypher_text").value;
    let key = document.getElementById("rsa_priv_key").value;

    sha_api(text, key, 'dec');
}
async function GetKeys(){
    let res = await fetch(backendIp + "/rsa");    
    let data = await res.json();
    document.getElementById("rsa_pub_key").setAttribute('disabled', '');
    document.getElementById("rsa_pub_key").value = data.data.public_key;
    document.getElementById("rsa_priv_key").setAttribute('disabled', '');
    document.getElementById("rsa_priv_key").value = data.data.private_key;
}
async function sha_api(text, key, type){
    
    let res = await fetch(backendIp + "/rsa", {
        headers: {
            'Accept': 'aplication/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({
            'text': text,
            'key': key,
            'type' : type
    })});
    let data = await res.json();

    if(type == 'enc'){
        document.getElementById("rsa_cypher_text").value = data['data'];
        document.getElementById("rsa_plain_text").value = ""
    }
    else{
        document.getElementById("rsa_plain_text").value = data['data']
        document.getElementById("rsa_cypher_text").value = ""
    }
    
}
function OpenBox(whatToShow){
    if(whatToShow == "MD5"){

        document.getElementById("MD5Container").classList.add("appear");
        document.getElementById("AESContainer").classList.remove("appear");
        document.getElementById("SHAContainer").classList.remove("appear");
    }
    else if(whatToShow == "AES"){

        document.getElementById("MD5Container").classList.remove("appear");
        document.getElementById("AESContainer").classList.add("appear");
        document.getElementById("SHAContainer").classList.remove("appear");
    }else if(whatToShow == "SHA"){

        document.getElementById("MD5Container").classList.remove("appear");
        document.getElementById("AESContainer").classList.remove("appear");
        document.getElementById("SHAContainer").classList.add("appear");
    }

}