<?php
// Include app file
include 'app.php';

// Destroy the session to log out the user
session_destroy();

// Redirect to the login page or any other desired location after logout
header('Location: index.php');
exit();
