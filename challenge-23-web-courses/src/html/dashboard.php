<?php
// Include app file
include 'app.php';

// Redirect to login page if not logged in
requireLoggedIn();
?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Dashboard</title>

	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/united/bootstrap.min.css" integrity="sha512-jILIYLO3ic8y+simzr0CPA46HZ3EM3Rwjf7WoWFee1mnY3Nel6FDM5Y1AZsc42PzZVcas8eINNwP+IMQbS+7XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
	<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
	<nav class="navbar bg-body-tertiary">
		<div class="container">
			<a class="navbar-brand" href="index.php"><i class="fa-solid fa-book-open"></i> WebCourses</a>
			<div class="collapse navbar-collapse" id="navbarNav">
			</div>
			<ul class="navbar-nav ml-auto">
				<li class="nav-item">
					<a class="nav-link" href="logout.php"><i class="fa-solid fa-right-from-bracket"></i> Logout</a>
				</li>
			</ul>
		</div>
	</nav>
	<div class="container">
		<h4 class="my-4">Welcome to the Dashboard, <?php echo htmlspecialchars($_SESSION['user_name']); ?>!</h4>
		<?php if ($_SESSION['user_name'] == 'admin') { ?>
		<div class="my-2">
			<div class="alert alert-warning">
				<strong>Administrator Access!</strong> <?=htmlspecialchars($flag);?>
			</div>
		</div>
		<?php } ?>
		<div class="my-2">
			<p>Select a course to view or upload assignments:</p>

			<div class="row">
			<?php
				$result = $database->query('SELECT * FROM courses');
				while ($row = $result->fetchArray()) {
			?>
				<div class="card my-2">
					<div class="card-body">
						<h5 class="card-title"><?php echo $row['icon'] . ' ' . $row['name']; ?></h5>
						<p class="card-text"><?php echo $row['description']; ?></p>
						<a href="course.php?id=<?php echo $row['id']; ?>" class="btn btn-outline-primary btn-sm">Course Page <i class="fa-solid fa-arrow-right-long"></i></a>
					</div>
				</div>
			<?php
				}
			?>
			</div>

		</div>
		<div class="my-4">
			<small>Copyright &copy; <?php echo date('Y'); ?></small>
		</div>
	</div>
</body>
</html>
