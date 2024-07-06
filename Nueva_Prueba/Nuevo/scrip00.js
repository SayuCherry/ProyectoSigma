alert("Hola mundo"); 
console.log("hola");

document.getElementById("btn__register").addEventListener("click", Register); 

//declaracion de variables 
var contenedor_login_register = document.querySelector(".contenedor__login-register"); 
var formulario_login = document.querySelector(".formulario__login"); 
var formulario_register = document.querySelector(".formulario__register"); 
var caja_trasera_login = document.querySelector(".caja__trasera-login"); 
var caja_trasera_register = document.querySelector(".caja__trasera-register"); 

function Register(){
 formulario_register.style.display = "block" ; //clik al boton de register
 contenedor_login_register.style.left = "410px" ; // form
 formulario_login.style.display = "none";
 caja_trasera_register.style.opacity = "0";
 caja_trasera_login.style.opacity = "1";

}