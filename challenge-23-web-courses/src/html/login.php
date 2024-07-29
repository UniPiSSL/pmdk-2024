<?php
// Include app file
include 'app.php';

// Redirect to dashboard page if logged in
requireLoggedOut();

// Check if the form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	// Retrieve user input
	$username = isset($_POST['username']) ? $_POST['username'] : '';
	$password = isset($_POST['password']) ? $_POST['password'] : '';

	// Validate user credentials
	$result = $database->query("SELECT * FROM users WHERE username = '$username' AND password = '$password';");
	
	// If valid credentials, log in the user
	if ($row = $result->fetchArray()) {
		$_SESSION['user_id'] = $row['id'];
		$_SESSION['user_name'] = $row['username'];
		header('Location: dashboard.php'); // Redirect to the dashboard or home page after successful login
		exit();
	} else {
		$error = 'Invalid username or password.';
	}
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Login</title>

	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/united/bootstrap.min.css" integrity="sha512-jILIYLO3ic8y+simzr0CPA46HZ3EM3Rwjf7WoWFee1mnY3Nel6FDM5Y1AZsc42PzZVcas8eINNwP+IMQbS+7XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
	<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
	<nav class="navbar bg-body-tertiary">
		<div class="container">
			<a class="navbar-brand" href="index.php"><i class="fa-solid fa-book-open"></i> WebCourses</a>
		</div>
	</nav>
	<div class="container">
		<h3 class="my-4"><i class="fa-solid fa-user"></i> Login</h3>
		<div class="my-2">
			<form method="POST">
				<div class="mb-3">
					<label for="username" class="form-label">Username</label>
					<input type="text" class="form-control" name="username" id="username">
				</div>
				<div class="mb-3">
					<label for="password" class="form-label">Password</label>
					<input type="password" class="form-control" name="password" id="password">
				</div>
				<button type="submit" class="btn btn-primary">Login</button>
			</form>
		</div>
		<div class="my-4">
			<p>Don't have an account? <a href="register.php">Register here</a></p>
		</div>
		<?php if (isset($error)) { ?>
			<div class="alert alert-danger" role="alert"><?php echo($error); ?></div>
		<?php } ?>
		<div class="my-4">
			<small>Copyright &copy; <?php echo date('Y'); ?></small>
		</div>
	</div>
</body>
</html>
