#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const express = require('express');
const jwt = require('jsonwebtoken');
const router = express.Router();
const { getSession, isAdminSession } = require('../utils/authorization.js');

// Load flag
const flag = (function (flag_path) {
    // Load flag from file
    if (fs.existsSync(flag_path)) {
        return fs.readFileSync(flag_path, 'utf8').trim();
    }
    // Load Test Flag
    return 'FLAG{example-flag-for-testing}';
})(path.join(__dirname, '..', 'flag.txt'));


// Default Page
router.get('/', (req, res) => {
    return res.render('index');
});

// Dashboard Page
router.get('/dashboard', (req, res) => {
    const sess = getSession(req);
    if (!sess) {
        return res.redirect('/');
    }

    return res.render('dashboard', { title: 'Nodelab ~ Πάνελ'});
});

// Profile Page
router.get('/profile', (req, res) => {
    const sess = getSession(req);
    if (!sess) {
        return res.redirect('/');
    }

    return res.render('profile', { title: 'Nodelab ~ Προφίλ', currentUser: sess.username, currentSchool: sess.school });
});

// Admin Page
router.get('/administration', (req, res) => {
    const sess = getSession(req);
    if (!sess) {
        return res.redirect('/');
    }

    try {
        if (isAdminSession(sess)) {
            return res.render('admin', { title: 'Nodelab ~ Admin', flag: flag });
        }
        else {
            return res.status(403).render('error', {error_code: '403', error_message: 'Access Denied'});
        }
    }
    catch (e) {
        return res.status(500);
    }

});

module.exports = router;
