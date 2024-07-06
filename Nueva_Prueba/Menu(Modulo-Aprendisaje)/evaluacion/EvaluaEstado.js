
document.addEventListener("DOMContentLoaded", function() {
    var cornerMarker = document.getElementById("Estado");
    var evaluarButton = document.querySelector(".button-evaluar");
    
    cornerMarker.style.backgroundColor = "white";

    evaluarButton.addEventListener("click", function() {
        
        var condition = true;  
        
        if (condition) {
            cornerMarker.style.backgroundColor = "green";  
        } else {
            cornerMarker.style.backgroundColor = "red";  
        }
    });
});
