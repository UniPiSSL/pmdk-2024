#!/usr/bin/env node

const express = require('express');
const router = express.Router();
const { getSession, signToken, verifyToken } = require('../utils/authorization.js');

// Handle error messages that database.js might return 
error_messages = [
	'Το όνομα χρήστη έχει ήδη ληφθεί',
	'Δόθηκε λάθος κωδικός πρόσβασης',
	'Εντοπίστηκε κακόβουλη ενέργεια',
	'Δεν δόθηκαν έγκυρα πεδία για ενημέρωση',
	'Δεν βρέθηκε σημείωηση με το συγκεκριμένο UUID'
]

// User Registration
router.post('/auth/register', async (req, res) => {
	try {
		const { username, school, password } = req.body;
		if (!username || !school || !password) {
			return res.status(401).json({ error: 'Παρακαλώ συμπληρώστε όλα τα απαραίτητα πεδία' });
		}
		else if (username.length > 20 || school.length > 20) {
			return res.status(401).json({ error: 'Το όνομα χρήστη ή το όνομα σχολείου δεν μπορεί να υπερβαίνει τους 20 χαρακτήρες' });
		}
		else if (password.length < 6) {
			return res.status(401).json({ error: 'Το μήκος του κωδικού πρόσβασης πρέπει να είναι τουλάχιστον 6 χαρακτήρες'});
		}
		await req.db.registerUser(username, school, password, 'user');
		return res.status(200).json({ message: 'Ο χρήστης εγγράφηκε με επιτυχία' });
	}
	catch (e) {
		if (error_messages.includes(e.message)) {
			return res.status(409).json({ error: e.message });
		}
		else {
			return res.status(500).json({ error: 'Εσωτερικό σφάλμα διακομιστή' });
		}
	}
});

// User Login
router.post('/auth/login', async (req, res) => {
	try {
		const { username, password } = req.body;
		const user = await req.db.loginUser(username, password);
		if (!user) {
			return res.status(401).json({ error: 'Μη έγκυρα διαπιστευτήρια σύνδεσης' });
		}

		const jwt = signToken(user);
		res.cookie('token', jwt, { httpOnly: true, maxAge: 3600000 });
		return res.status(200).json({ message: 'Η σύνδεση ήταν επιτυχής'});
	}
	catch (e) {
		res.status(500).json({ error: 'Εσωτερικό σφάλμα διακομιστή' });
	}
});

// User Logout
router.get('/auth/logout', async (req, res) => {
	try {
		res.cookie('token', '');
		return res.redirect('/');
	}
	catch (e) {
		return res.status(500).json({ error: 'Εσωτερικό σφάλμα διακομιστή'});
	}
});

// Update User Information
router.put('/auth/update', async (req, res) => {
	try {
		const sess = getSession(req);
		const { currentPassword, updates } = req.body;
		if (!sess) {
			return res.status(401).json({ error: 'Μη εξουσιοδοτημένη ενέργεια' })
		}

		if ((updates.username && updates.username.length > 20) || (updates.school && updates.school.length > 20)) {
			return res.status(401).json({ error: 'Το όνομα χρήστη ή το όνομα σχολείου δεν μπορεί να υπερβαίνει τους 20 χαρακτήρες' });
		}
		else if (updates.password && updates.password.length < 6) {
			return res.status(401).json({ error: 'Το μήκος του κωδικού πρόσβασης πρέπει να είναι τουλάχιστον 6 χαρακτήρες'});
		}
		
		await req.db.updateUser(sess.id, currentPassword, updates);
		return res.status(200).json({ message: 'Επιτυχής ενημέρωση χρήστη. Παρακαλούμε συνδεθείτε ξανά για να τεθούν σε ισχύ οι αλλαγές'});
	}
	catch (e) {
		if (error_messages.includes(e.message)) {
			return res.status(401).json({ error: e.message }); 
		}
		else {
			return res.status(500).json({ error: 'Εσωτερικό σφάλμα διακομιστή' });
		}
	}
});

// Add Note
router.post('/note/add', async (req, res) => {
	try {
		const sess = getSession(req);
		const { title, content } = req.body;
		if (!sess) {
			return res.status(401).json({ error: 'Μη εξουσιοδοτημένη ενέργεια' });
		}

		if (!title) {
			return res.status(401).json({ error: 'Το πεδίο τίτλου δεν έχει καθοριστεί' });
		}
		else if (!content) {
			return res.status(401).json({ error: 'Το πεδίο περιεχομένου δεν έχει καθοριστεί' });
		}
		else if (title.length > 50) {
			return res.status(401).json({ error: 'Το μήκος του τίτλου δεν μπορεί να υπερβαίνει τους 50 χαρακτήρες' });
		}
		else if (content.length > 500) {
			return res.status(401).json({ error: 'Το μήκος του περιεχομένου δεν μπορεί να υπερβαίνει τους 500 χαρακτήρες' });
		}

		const note = await req.db.addNote(sess.id, title, content);
		return res.status(200).json({ addedNote: note });
	}
	catch (e) {
		if (error_messages.includes(e.message)) {
			return res.status(401).json({ error: e.message }); 
		}
		else {
			return res.status(500).json({ error: 'Εσωτερικό σφάλμα διακομιστή' });
		}
	}
});

// Delete Note
router.delete('/note/delete', async (req, res) => {
	try {
		const sess = getSession(req);
		const { uuid } = req.body;
		
		if (!sess) {
			return res.status(401).json({ error: 'Μη εξουσιοδοτημένη ενέργεια' });
		}

		await req.db.deleteNote(uuid, sess.id);
		return res.status(200).json({ message: 'Η σημείωση διαγράφηκε με επιτυχία'})
	}
	catch (e) {
		if (error_messages.includes(e.message)) {
			return res.status(400).json({ error: e.message });
		}
		else {
			return res.status(500).json({ error: 'Εσωτερικό σφάλμα διακομιστή' });
		}
	}
});

// Get all notes
router.get('/note/all', async (req, res) => { 
	try {
		const sess = getSession(req);
		if (!sess) {
			return res.status(401).json({ error: 'Μη εξουσιοδοτημένη ενέργεια' });
		}
		
		const notes = await req.db.getNotes(sess.id);
		return res.status(200).json({ notes });
	}
	catch (e) {
		return res.status(500).json({ error: 'Εσωτερικό σφάλμα διακομιστή' });
	}
});

module.exports = router;
