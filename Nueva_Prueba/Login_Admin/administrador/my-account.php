<!DOCTYPE html>
<html lang="es">

<head>
	<title>Mis Datos</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">
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
							<a href="user.php"><i class="zmdi zmdi-male-female zmdi-hc-fw"></i> Usuarios</a>
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
					<a href="search.php" class="btn-search">
						<i class="zmdi zmdi-search"></i>
					</a>
				</li>
			</ul>
		</nav>
		<!-- Content page -->
		<div class="container-fluid">
			<div class="page-header">
				<h1 class="text-titles"><i class="zmdi zmdi-settings zmdi-hc-fw"></i> MI CUENTA</small></h1>
			</div>
			<p style="color:white" class="lead">Bienvenido a la configuración de la cuenta</p>
		</div>

		<!-- Panel mi cuenta -->
		<div class="container-fluid">
			<div class="panel panel-success">
				<div class="panel-heading">
					<h3 class="panel-title"><i class="zmdi zmdi-refresh"></i> &nbsp; MI CUENTA</h3>
				</div>
				<div class="panel-body">
					<form>
						<fieldset>
							<legend style="color:white"><i class="zmdi zmdi-key" style="color:white;"></i> &nbsp; Datos de la cuenta</legend>
							<div class="container-fluid">
								<div class="row">
									<div class="col-xs-12">
										<div class="form-group label-floating">
											<label class="control-label">Nombre de usuario *</label>
											<input pattern="[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]{1,15}" class="form-control" type="text" name="usuario-up" required="" maxlength="15">
										</div>
									</div>
									<div class="col-xs-12 col-sm-6">
										<div class="form-group label-floating">
											<label class="control-label">Correo</label>
											<input class="form-control" type="email" name="email-up" maxlength="50">
										</div>
									</div>
									<div class="col-xs-12">
										<div class="form-group">
											<label class="control-label">Genero</label>
											<div class="radio radio-primary">
												<label>
													<input type="radio" name="optionsGenero" id="optionsRadios1" value="Masculino" checked="">
													<i class="zmdi zmdi-male-alt"></i> &nbsp; Masculino
												</label>
											</div>
											<div class="radio radio-primary">
												<label>
													<input type="radio" name="optionsGenero" id="optionsRadios2" value="Femenino">
													<i class="zmdi zmdi-female"></i> &nbsp; Femenino
												</label>
											</div>
										</div>
									</div>
								</div>
							</div>
						</fieldset>
						<br>
						<fieldset>
							<legend style="color:white"><i style="color:white" class="zmdi zmdi-lock"></i> &nbsp; Contraseña</legend>
							<p style="color:white">
								Configuración de contraseña
							</p>
							<div class="container-fluid">
								<div class="row">
									<div class="col-xs-12">
										<div class="form-group label-floating">
											<label class="control-label">Contraseña actual *</label>
											<input class="form-control" type="password" name="password-up" required="" maxlength="70">
										</div>
									</div>
									<div class="col-xs-12 col-sm-6">
										<div class="form-group label-floating">
											<label class="control-label">Nueva contraseña *</label>
											<input class="form-control" type="password" name="newPassword1-up" required="" maxlength="70">
										</div>
									</div>
									<div class="col-xs-12 col-sm-6">
										<div class="form-group label-floating">
											<label class="control-label">Repita la nueva contraseña *</label>
											<input class="form-control" type="password" name="newPassword2-up" required="" maxlength="70">
										</div>
									</div>
								</div>
							</div>
						</fieldset>
						<br>
						<fieldset>
							<legend style="color:white"><i style="color:white" class="zmdi zmdi-star"></i> &nbsp; Nivel de privilegios</legend>
							<div class="container-fluid">
								<div class="row">
									<div class="col-xs-12 col-sm-6" style="color:white">
										<p class="text-left" style="color:white">
										<div style="color:white" class="label label-success">Nivel 1</div> Control total del sistema
										</p>
										<p class="text-left" style="color:white">
										<div style="color:white" class="label label-primary">Nivel 2</div> Permiso para actualización y registro
										</p>
										<p class="text-left" style="color:white">
										<div style="color:white" class="label label-info">Nivel 3</div> Permiso para registro
										</p>
									</div>
									<div class="col-xs-12 col-sm-6">
										<div class="radio radio-primary">
											<label>
												<input type="radio" name="optionsPrivilegio" id="optionsRadios1" value="1">
												<i class="zmdi zmdi-star"></i> &nbsp; Nivel básico
											</label>
										</div>
										<div class="radio radio-primary">
											<label>
												<input type="radio" name="optionsPrivilegio" id="optionsRadios2" value="2">
												<i class="zmdi zmdi-star"></i> &nbsp; Nivel medio
											</label>
										</div>
										<div class="radio radio-primary">
											<label>
												<input type="radio" name="optionsPrivilegio" id="optionsRadios3" value="3" checked="">
												<i class="zmdi zmdi-star"></i> &nbsp; Nivel avanzado
											</label>
										</div>
									</div>
								</div>
							</div>
						</fieldset>
						<p class="text-center" style="margin-top: 20px;">
							<button type="submit" class="btn btn-success btn-raised btn-sm"><i class="zmdi zmdi-refresh"></i> Actualizar</button>
						</p>
					</form>
				</div>
			</div>
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
	</script>
</body>

</html>