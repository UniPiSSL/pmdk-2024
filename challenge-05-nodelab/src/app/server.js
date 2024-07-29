#!/usr/bin/env node

// Dependencies
const express = require('express');
const cookieParser = require('cookie-parser');
const pug = require('pug');

const Database = require('./utils/database');
const routeIndex = require('./routes/index');
const routeAPI = require('./routes/api');
const db = new Database('./database.db');

// App Setup
const app = express();
app.use(cookieParser());
app.use(express.json());
app.use(express.static('static'));
app.set('view engine', 'pug');

app.use('/', routeIndex);
app.use('/api', (req, res, next) => {
	req.db = db;
	next();
}, routeAPI);

// Handle app errors
app.all('*', (req, res) => {
	return res.status(404).render('error', {error_code: '404', error_message: 'Η σελίδα δεν βρέθηκε'});
});

app.use((err, req, res, next) => {
	return res.status(500).render('error', {error_code: '500', error_message: 'Εσωτερικό σφάλμα διακομιστή'});
});

(async() => {
	// Initialise Database
	await db.connect();
	await db.migrate();

	// Start Server
	const port = process.env.APP_PORT || 8000;
	app.listen(port, () => console.log(`[+] Nodelab is running on port ${port}`));
})();
