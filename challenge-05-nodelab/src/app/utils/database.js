#!/usr/bin/env node

const sqlite3 = require('sqlite3');
const { open } = require('sqlite');
const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid');

class Database {
	constructor(db_file) {
		this.db_file = db_file;
		this.db = undefined;
	}

	async connect() {
		this.db = await open({
			filename: this.db_file,
			driver: sqlite3.Database
		});
	}

	async migrate() {
		await this.db.exec(`
			DROP TABLE if exists users;
			DROP TABLE if exists notes;
		
			CREATE TABLE users (
				id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
				username TEXT UNIQUE,
				school TEXT,
				password TEXT,
				role TEXT
			);

			CREATE TABLE notes (
				uuid TEXT PRIMARY KEY,
				userId INTEGER,
				title TEXT,
				content TEXT,
				FOREIGN KEY (userId) REFERENCES users (id)
			);
		`);
	}

	async isUsernameTaken(username, excludingUserId = null) {
		let query = 'SELECT id FROM users WHERE username = ?';

		if (excludingUserId !== null) {
			query += ' AND id != ?';
			username.push(excludingUserId);
		}

		let stmt = await this.db.prepare(query);
		let user = await stmt.get(username);

		return user;

	}

	async getUserPassword(id) {
		let query = 'SELECT password FROM users WHERE id = ?';

		let stmt = await this.db.prepare(query);
		let pass = await stmt.get(id);
		return pass;
	}

	async registerUser(username, school, password, role) {
		if (await this.isUsernameTaken(username)) {
			throw new Error('Το όνομα χρήστη έχει ήδη ληφθεί');
		}

		const hashedPassword = await bcrypt.hash(password, 10);
		let stmt = await this.db.prepare('INSERT INTO users (username, school, password, role) VALUES (?, ?, ?, ?)');
		return await stmt.run(username, school, hashedPassword, role);
	}

	async loginUser(username, password) {
		let stmt = await this.db.prepare('SELECT * FROM users WHERE username = ?');
		let user = await stmt.get(username);

		if (user && await bcrypt.compare(password, user.password)) {
			return {'id': user.id, 'username': user.username, 'school': user.school, 'role': user.role};
		}
		else {
			return null;
		}
	}

	async updateUser(id, currentPassword, updates) {
		let fields = [];
		let values = [];
		let userPassword = await this.getUserPassword(id);
		
		if (!(await bcrypt.compare(currentPassword, userPassword.password))) {
			throw new Error('Δόθηκε λάθος κωδικός πρόσβασης');
		}

		for (const [key, value] of Object.entries(updates)) {
			if (key.toLowerCase() === 'username' && (await this.isUsernameTaken(value))) {
				throw new Error('Το όνομα χρήστη έχει ήδη ληφθεί');
			}
			else if (key.toLowerCase() === 'password' && value) {
				fields.push(`${key} = ?`);
				values.push(await bcrypt.hash(value, 10));
			}
			else if (key.toLowerCase() === 'role') {
				throw new Error('Εντοπίστηκε κακόβουλη ενέργεια');
			}
			else {
				fields.push(`${key} = ?`);
				values.push(value);
			}
		}

		if (fields.length === 0) {
			throw new Error('Δεν δόθηκαν έγκυρα πεδία για ενημέρωση');
		}

		const query = `UPDATE users SET ${fields.join(', ')} WHERE id = ?`;
		values.push(id);
		let stmt = await this.db.prepare(query);
		return await stmt.run(values);
	}

	async addNote(userId, title, content) {
		let stmt = await this.db.prepare('INSERT INTO notes (uuid, userId, title, content) VALUES (?, ?, ?, ?)');
		let uuid = uuidv4();
		let result = await stmt.run(uuid, userId, title, content);

		if (result.changes === 1) {
			const selectStmt = await this.db.prepare('SELECT * FROM notes WHERE uuid = ?');
			const insertedData = await selectStmt.get(uuid);

			return insertedData;
		}
	}

	async deleteNote(uuid, userId) {
		let stmt = await this.db.prepare('DELETE FROM notes WHERE uuid = ? AND userId = ?');
		let result = await stmt.run(uuid, userId);
		if (result.changes > 0) {
			return true;
		}
		else {
			throw new Error('Δεν βρέθηκε σημείωηση με το συγκεκριμένο UUID');
		}
	}

	async getNotes(id) {
		let stmt = await this.db.prepare('SELECT * FROM notes WHERE userId = ?');
		return await stmt.all(id);
	}

}

module.exports = Database;
