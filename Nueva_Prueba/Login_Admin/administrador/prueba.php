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
                        <a href="my-data.html" title="Mis datos">
                            <i class="zmdi zmdi-account-circle"></i>
                        </a>
                    </li>
                    <li>
                        <a href="my-account.html" title="Mi cuenta">
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
                    <a href="home.html">
                        <i class="zmdi zmdi-view-dashboard zmdi-hc-fw"></i> Dashboard
                    </a>
                </li>
                <li>
                    <a href="#!" class="btn-sideBar-SubMenu">
                        <i class="zmdi zmdi-account-add zmdi-hc-fw"></i> Usuarios <i class="zmdi zmdi-caret-down pull-right"></i>
                    </a>
                    <ul class="list-unstyled full-box">
                        <li>
                            <a href="admin.html"><i class="zmdi zmdi-account zmdi-hc-fw"></i> Administradores</a>
                        </li>
                        <li>
                            <a href="user.html"><i class="zmdi zmdi-male-female zmdi-hc-fw"></i> Clientes</a>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </section>

    <!-- Content page-->
    <section class="full-box dashboard-contentPage">
        <!-- NavBar -->
        <nav class="full-box dashboard-Navbar">
            <ul class="full-box list-unstyled text-right">
                <li class="pull-left">
                    <a href="#!" class="btn-menu-dashboard"><i class="zmdi zmdi-more-vert"></i></a>
                </li>
                <li>
                    <a href="search.html" class="btn-search">
                        <i class="zmdi zmdi-search"></i>
                    </a>
                </li>
            </ul>
        </nav>

        <!-- Content page -->
        <div class="container-fluid">
            <div class="page-header">
                <h1 class="text-titles">Sistema <small>Usuarios</small></h1>
            </div>
        </div>
        <div class="full-box text-center" style="padding: 30px 10px;">
            <article class="full-box tile">
                <div class="full-box tile-title text-center text-titles text-uppercase">
                    Administradores
                </div>
                <div class="full-box tile-icon text-center">
                    <i class="zmdi zmdi-account"></i>
                </div>
                <div class="full-box tile-number text-titles">
                    <p class="full-box">7</p>
                    <small>Registrados</small>
                </div>
            </article>
            <article class="full-box tile">
                <div class="full-box tile-title text-center text-titles text-uppercase">
                    Estudiantes
                </div>
                <div class="full-box tile-icon text-center">
                    <i class="zmdi zmdi-face"></i>
                </div>
                <div class="full-box tile-number text-titles">
                    <p class="full-box">70</p>
                    <small>Registrados</small>
                </div>
            </article>
        </div>
        <div class="container-fluid">
            <div class="page-header">
                <h1 class="text-titles">Sistema <small>Linea de Tiempo - Inicio de Sesión</small></h1>
            </div>

            <!-- ComboBox para seleccionar semanas -->
            <div class="form-group">
                <label for="weekSelector">Selecciona una semana:</label>
                <select id="weekSelector" class="form-control" onchange="updateTimeline()">
                    <option value="1">Semana 1</option>
                    <option value="2">Semana 2</option>
                    <option value="3">Semana 3</option>
                    <option value="4">Semana 4</option>
                </select>
            </div>
            <!-- Línea de tiempo -->
            <section id="cd-timeline" class="cd-container">
                <!-- Aquí se actualizará el contenido de la línea de tiempo -->
            </section>
        </div>
    </section>

    <!--====== Scripts -->
    <script src="./js/jquery-3.1.1.min.js"></script>
    <script src="./js/sweetalert2.min.js"></script>
    <script src="./js/bootstrap.min.js"></script>
    <script src="./js/material.min.js"></script>
    <script src="./js/ripples.min.js"></script>
    <script src="./js/jquery.mCustomScrollbar.concat.min.js"></script>
    <script src="./js/main.js"></script>
    <script>
        $.material.init();

        // Datos de ejemplo para cada semana
        const timelineData = {
            1: [{
                    imgSrc: 'assets/avatars/StudetMaleAvatar.png',
                    title: '1 - Name (Admin)',
                    startTime: '7:00 AM',
                    endTime: '7:17 AM',
                    date: '07/07/2016'
                },
                {
                    imgSrc: 'assets/avatars/StudetMaleAvatar.png',
                    title: '2 - Name (Teacher)',
                    startTime: '7:30 AM',
                    endTime: '7:47 AM',
                    date: '07/07/2016'
                }
            ],
            2: [{
                    imgSrc: 'assets/avatars/StudetMaleAvatar.png',
                    title: '3 - Name (Student)',
                    startTime: '8:00 AM',
                    endTime: '8:17 AM',
                    date: '14/07/2016'
                },
                {
                    imgSrc: 'assets/avatars/StudetMaleAvatar.png',
                    title: '4 - Name (Personal Ad.)',
                    startTime: '8:30 AM',
                    endTime: '8:47 AM',
                    date: '14/07/2016'
                }
            ],
            3: [{
                    imgSrc: 'assets/avatars/StudetMaleAvatar.png',
                    title: '5 - Name (Admin)',
                    startTime: '9:00 AM',
                    endTime: '9:17 AM',
                    date: '21/07/2016'
                },
                {
                    imgSrc: 'assets/avatars/StudetMaleAvatar.png',
                    title: '6 - Name (Teacher)',
                    startTime: '9:30 AM',
                    endTime: '9:47 AM',
                    date: '21/07/2016'
                }
            ],
            4: [{
                    imgSrc: 'assets/avatars/StudetMaleAvatar.png',
                    title: '7 - Name (Student)',
                    startTime: '10:00 AM',
                    endTime: '10:17 AM',
                    date: '28/07/2016'
                },
                {
                    imgSrc: 'assets/avatars/StudetMaleAvatar.png',
                    title: '8 - Name (Personal Ad.)',
                    startTime: '10:30 AM',
                    endTime: '10:47 AM',
                    date: '28/07/2016'
                }
            ]
        };

        function updateTimeline() {
            const selectedWeek = document.getElementById('weekSelector').value;
            const timelineContainer = document.getElementById('cd-timeline');

            // Limpiar la línea de tiempo actual
            timelineContainer.innerHTML = '';

            // Añadir los nuevos elementos de la línea de tiempo
            if (timelineData[selectedWeek]) {
                timelineData[selectedWeek].forEach(event => {
                    const block = document.createElement('div');
                    block.className = 'cd-timeline-block';

                    const imgDiv = document.createElement('div');
                    imgDiv.className = 'cd-timeline-img';
                    const img = document.createElement('img');
                    img.src = event.imgSrc;
                    img.alt = 'Picture';
                    imgDiv.appendChild(img);

                    const contentDiv = document.createElement('div');
                    contentDiv.className = 'cd-timeline-content';
                    const title = document.createElement('h4');
                    title.innerText = event.title;
                    const p = document.createElement('p');
                    p.innerText = `${event.startTime} - ${event.endTime}`;
                    const span = document.createElement('span');
                    span.className = 'cd-date';
                    span.innerText = event.date;

                    contentDiv.appendChild(title);
                    contentDiv.appendChild(p);
                    contentDiv.appendChild(span);

                    block.appendChild(imgDiv);
                    block.appendChild(contentDiv);

                    timelineContainer.appendChild(block);
                });
            }
        }

        // Inicializar la línea de tiempo con la primera semana
        updateTimeline();
    </script>
</body>

</html>