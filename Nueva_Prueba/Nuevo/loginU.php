<?php
include 'login00.php'; 

$correo = $_POST['correo']; 
$contrasena = $_POST['contrasena']; 
$query= "SELECT * FROM loginR WHERE correo='$correo' AND contrasena= '$contrasena'"; 
$ejecutar = mysqli_query($conn, $query); 


if ($ejecutar->num_rows > 0) {
    // El usuario existe
    $_SESSION['correo'] = $correo;
    $_SESSION['comtrasena'] = $contrasena;
    
    
        header("Location: ../Menu(Modulo-Aprendisaje)/Menu.html");
    
} else {
    // El usuario no existe
    echo "Correo o contraseña incorrecto.";
}

?>