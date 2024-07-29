<?php

// Disable errors
#error_reporting(0);
#ini_set('display_errors', 0);


// Initialize SQLite database
$database = '../database.db';

// Check if the database file exists
if (!file_exists($database)) {
	// Create empty file
	$handle = fopen($database, 'w');

	// Check if file creation was successful
	if ($handle === false) {
		die('Unable to create the database file.');
	} else {
		fclose($handle);
	}

	$database = new SQLite3($database);

	// Create users table if not exists
	$database->exec('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)');

	// Create courses table if not exists
	$database->exec('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, icon TEXT, name TEXT, description TEXT)');

	// Init database content
	$init_courses = [
		['<i class="fa-solid fa-square-root-variable"></i>', 'Mathematics', 'Mathematics courses cover a broad range of topics, including algebra, calculus, geometry, and statistics. Students will develop problem-solving skills, logical reasoning, and a deep understanding of mathematical principles. This foundational discipline is crucial for various fields, from science and engineering to economics and technology.'],
		['<i class="fa-solid fa-atom"></i>', 'Physics', 'Physics courses delve into the fundamental principles that govern the behavior of matter and energy in the universe. Students will explore classical mechanics, electromagnetism, thermodynamics, and modern physics concepts. Through hands-on experiments and theoretical study, participants will gain insights into the laws governing the physical world.'],
		['<i class="fa-solid fa-dna"></i>', 'Biology', 'Biology courses focus on the study of living organisms and their interactions with the environment. Participants will explore topics such as genetics, ecology, physiology, and microbiology. These courses provide a comprehensive understanding of life sciences, applicable in fields like medicine, research, environmental science, and biotechnology.'],
		['<i class="fa-solid fa-computer"></i>', 'Computer Science', 'Computer Science courses equip individuals with the knowledge and skills needed to understand and develop software, algorithms, and computational systems. Participants will learn programming languages, data structures, algorithms, and software development methodologies. This field is essential for a wide range of industries, including technology, finance, healthcare, and artificial intelligence.']
	];
	$stmt = $database->prepare('INSERT INTO courses (icon, name, description) VALUES (:icon, :name, :description)');
	foreach ($init_courses as $course) {
		$stmt->bindParam(':icon', $course[0], SQLITE3_TEXT);
		$stmt->bindParam(':name', $course[1], SQLITE3_TEXT);
		$stmt->bindParam(':description', $course[2], SQLITE3_TEXT);
		$stmt->execute();
	}
	$init_course_id = $database->lastInsertRowID();

	$init_users = [
		['admin', generateRandomString(32)]
	];
	$stmt = $database->prepare('INSERT INTO users (username, password) VALUES (:username, :password)');
	foreach ($init_users as $user) {
		$stmt->bindParam(':username', $user[0], SQLITE3_TEXT);
		$stmt->bindParam(':password', $user[1], SQLITE3_TEXT);
		$stmt->execute();
	}
}
else {
	$database = new SQLite3($database);
}

// Load Flag
$flag = trim(file_get_contents('../flag.txt'));




// Start session
session_start();

// Function to check if a user is logged in
function isUserLoggedIn() {
	return isset($_SESSION['user_id']);
}

// Function to redirect to login if not logged in
function requireLoggedIn() {
	if (!isUserLoggedIn()) {
		header('Location: login.php');
		exit();
	}
}

// Function to redirect to dashboard if logged in
function requireLoggedOut() {
	if (isUserLoggedIn()) {
		header('Location: dashboard.php');
		exit();
	}
}

// Function to generate random string
function generateRandomString($length = 10) {
    return substr(str_shuffle(str_repeat($x='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', ceil($length/strlen($x)) )),1,$length);
}
