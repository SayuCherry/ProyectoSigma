<!DOCTYPE html>
<html lang="es">

<head>
    <title>Inicio</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="./css/main.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>
    <!-- SideBar -->
    <section class="full-box cover dashboard-sideBar">
        <div class="full-box dashboard-sideBar-bg btn-menu-dashboard"></div>
        <div class="full-box dashboard-sideBar-ct">
            <!--SideBar Title -->
            <div class="full-box text-uppercase text-center text-titles dashboard-sideBar-title">
                SIGMA <i class="zmdi zmdi-close btn-menu-dashboard visible-xs"></i>
            </div>
            <!-- SideBar User info -->
            <div class="full-box dashboard-sideBar-UserInfo">
                <figure class="full-box">
                    <img src="./assets/avatars/AdminMaleAvatar.png" alt="UserIcon">
                    <figcaption class="text-center text-titles">Usuario</figcaption>
                </figure>
                <ul class="full-box list-unstyled text-center">
                    <li>
                        <a href="my-data.php" title="Mis datos">
                            <i class="zmdi zmdi-account-circle"></i>
                        </a>
                    </li>
                    <li>
                        <a href="my-account.php" title="Mi cuenta">
                            <i class="zmdi zmdi-settings"></i>
                        </a>
                    </li>
                    <li>
                        <a href="#!" title="Salir del sistema" class="btn-exit-system">
                            <i class="zmdi zmdi-power"></i>
                        </a>
                    </li>
                </ul>
            </div>
            <!-- SideBar Menu -->
            <ul class="list-unstyled full-box dashboard-sideBar-Menu">
                <li>
                    <a href="home.php">
                        <i class="zmdi zmdi-view-dashboard zmdi-hc-fw"></i> Dashboard
                    </a>
                </li>
                <li>
                    <a href="#!" class="btn-sideBar-SubMenu">
                        <i class="zmdi zmdi-account-add zmdi-hc-fw"></i> Usuarios <i class="zmdi zmdi-caret-down pull-right"></i>
                    </a>
                    <ul class="list-unstyled full-box">
                        <li>
                            <a href="admin.php"><i class="zmdi zmdi-account zmdi-hc-fw"></i> Administradores</a>
                        </li>
                        <li>
                            <a href="user.php"><i class="zmdi zmdi-male-female zmdi-hc-fw"></i> Clientes</a>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </section>
    
    <!-- Content page-->
    <section class="full-box dashboard-contentPage">
    <nav class="full-box dashboard-Navbar">
			<ul class="full-box list-unstyled text-right">
				<li class="pull-left">
					<a href="#!" class="btn-menu-dashboard"><i class="zmdi zmdi-more-vert"></i></a>
				</li>
				<li>
					<a href="search.php" class="btn-search">
						<i class="zmdi zmdi-search"></i>
					</a>
				</li>
			</ul>
		</nav>
        <!-- NavBar -->
        <div class="container">
        <h1>Gráfico de Puntaje de Lenguaje de Manos</h1>
        <canvas id="puntajeChart" width="400" height="200"></canvas>
    </div>

    <div class="container">
        <h1>Gráfico de Usuarios</h1>
        <canvas id="usuariosChart" width="400" height="200"></canvas>
    </div>

    <div class="container">
        <h1>Gráfico de Administradores por Secciones</h1>
        <canvas id="adminChart" width="400" height="200"></canvas>
    </div>

    <script>
        // Datos ficticios para puntaje de lenguaje de manos
        const dataLenguajeManos = [
            { nombre: "Juan", puntaje: 85, fecha: "2023-01-01" },
            { nombre: "Ana", puntaje: 90, fecha: "2023-01-02" },
            { nombre: "Pedro", puntaje: 75, fecha: "2023-01-03" },
            { nombre: "Maria", puntaje: 95, fecha: "2023-01-04" },
            { nombre: "Luis", puntaje: 80, fecha: "2023-01-05" }
        ];

        // Datos ficticios para usuarios
        const dataUsuarios = [
            { seccion: "A", usuarios: 30 },
            { seccion: "B", usuarios: 50 },
            { seccion: "C", usuarios: 40 },
            { seccion: "D", usuarios: 60 },
            { seccion: "E", usuarios: 20 }
        ];

        // Datos ficticios para administradores por secciones
        const dataAdmin = [
            { seccion: "A", admin: 3 },
            { seccion: "B", admin: 5 },
            { seccion: "C", admin: 2 },
            { seccion: "D", admin: 4 },
            { seccion: "E", admin: 1 }
        ];

        // Extraer los datos necesarios para el gráfico de puntaje de lenguaje de manos
        const labelsLenguajeManos = dataLenguajeManos.map(row => row.nombre);
        const puntajesLenguajeManos = dataLenguajeManos.map(row => row.puntaje);

        // Extraer los datos necesarios para el gráfico de usuarios
        const labelsUsuarios = dataUsuarios.map(row => row.seccion);
        const usuarios = dataUsuarios.map(row => row.usuarios);

        // Extraer los datos necesarios para el gráfico de administradores por secciones
        const labelsAdmin = dataAdmin.map(row => row.seccion);
        const admin = dataAdmin.map(row => row.admin);

        // Crear el gráfico de puntaje de lenguaje de manos
        const ctxLenguajeManos = document.getElementById('puntajeChart').getContext('2d');
        const puntajeChart = new Chart(ctxLenguajeManos, {
            type: 'bar',
            data: {
                labels: labelsLenguajeManos,
                datasets: [{
                    label: 'Puntaje de Lenguaje de Manos',
                    data: puntajesLenguajeManos,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Crear el gráfico de usuarios
        const ctxUsuarios = document.getElementById('usuariosChart').getContext('2d');
        const usuariosChart = new Chart(ctxUsuarios, {
            type: 'line',
            data: {
                labels: labelsUsuarios,
                datasets: [{
                    label: 'Número de Usuarios',
                    data: usuarios,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Crear el gráfico de administradores por secciones
        const ctxAdmin = document.getElementById('adminChart').getContext('2d');
        const adminChart = new Chart(ctxAdmin, {
            type: 'pie',
            data: {
                labels: labelsAdmin,
                datasets: [{
                    label: 'Número de Administradores',
                    data: admin,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 255, 255, 1)',
                        'rgba(255, 255, 255, 1)',
                        'rgba(255, 255, 255, 1)',
                        'rgba(255, 255, 255, 1)',
                        'rgba(255, 255, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true
            }
        });
    </script>
   
    </section>

    <!--====== Scripts -->
    <script src="./js/jquery-3.1.1.min.js"></script>
    <script src="./js/sweetalert2.min.js"></script>
    <script src="./js/bootstrap.min.js"></script>
    <script src="./js/material.min.js"></script>
    <script src="./js/ripples.min.js"></script>
    <script src="./js/jquery.mCustomScrollbar.concat.min.js"></script>
    <script src="./js/main.js"></script>
    
    
</body>

</html>