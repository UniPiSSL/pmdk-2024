<?php
// Include app file
include 'app.php';

// Redirect user
if (isUserLoggedIn()) {
	header('Location: dashboard.php');
	exit();
}
else {
	header('Location: login.php');
	exit();
}
