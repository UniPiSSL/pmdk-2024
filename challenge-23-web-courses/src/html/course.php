<?php
// Include app file
include 'app.php';

// Redirect to login page if not logged in
requireLoggedIn();

// Check if course ID is provided in the URL
if (isset($_GET['id'])) {
	$courseId = intval($_GET['id']);

	// Retrieve course information
	$result = $database->query("SELECT * FROM courses WHERE id = $courseId");
	$course = $result->fetchArray();
	
	if (!$course) {
		// Redirect to dashboard if course not found
		header('Location: dashboard.php');
		exit();
	}
} else {
	// Redirect to dashboard if course ID not provided
	header('Location: dashboard.php');
	exit();
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Course - <?php echo $course['name']; ?></title>

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
		<h4 class="my-4"><?php echo $course['icon']; ?> <?php echo $course['name']; ?> - Course Page</h4>
		<div class="my-2">
			<p><?php echo $course['description']; ?></p>
		</div>
		<div class="my-4">
			<small>Copyright &copy; <?php echo date('Y'); ?></small>
		</div>
	</div>
</body>
</html>
