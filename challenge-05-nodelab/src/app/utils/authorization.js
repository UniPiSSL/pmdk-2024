#!/usr/bin/env node
const authSecret = require('crypto').randomBytes(64).toString('hex');
const jwt = require('jsonwebtoken');

const signToken = (payload) => {
	return jwt.sign(payload, authSecret);
};

const verifyToken = (token) => {
	try {
		return jwt.verify(token, authSecret);
	}
	catch (e) {
		return null;
	}
};

const getSession = (req) => {
    const token = req.cookies.token;
    const jwt = verifyToken(token);
    return jwt;
};

const isAdminSession = (sess) => {
	if (sess && sess.role === 'admin') {
		return true;
	}
	return false;
};


module.exports = {
	getSession,
	signToken,
	verifyToken,
	isAdminSession
};
