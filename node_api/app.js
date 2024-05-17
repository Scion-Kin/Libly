#!/usr/bin/env node

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const nodemailer = require('nodemailer');
const cors = require('cors');
const fs = require('fs');

// Middleware to parse JSON body
app.use(bodyParser.json());

app.use(cors()); // Cross origin enabled

const transporter = nodemailer.createTransport({
  host: 'smtp-relay.brevo.com',
  port: 587,
  auth: {
    user: process.argv[2],
    pass: process.argv[3]
  }
});

// Route to handle signup emailing
app.post('/signup', (req, res) => {
  try {
    let data = fs.readFileSync('confirmation_email.html', 'utf8');
    data = data.replace(/{% id %}/g, req.body.id);
    data = data.replace(/{% name %}/g, `${req.body.first_name} ${req.body.last_name}`);

    const mailOptions = {
      from: 'mugabo@centralbees.com',
      to: req.body.email,
      subject: 'Welcome to Libly! Please comfim your email.',
      text: data
    };

    transporter.sendMail(mailOptions, function (error, info) {
      if (error) {
        res.json({ error: 'Email sending failed' });
      } else {
        res.json({ success: 'Email sent successfully' });
      }
    });
  } catch (error) {
    res.status(500).json({ error });
  }
});

// Route for handling password reset emailing
app.post('/reset', (req, res) => {
  try {
    const mailOptions = {
      from: 'mugabo@centralbees.com',
      to: req.body.email,
      subject: `Password reset for ${req.body.name}`,
      text: `Your code is \n ${req.body.reset_code} \n If you didn't request this code, ignore this email.`
    };

    transporter.sendMail(mailOptions, function (error, info) {
      if (error) {
        res.json({ error: 'Email sending failed' });
      } else {
        res.json({ success: 'Email sent successfully' });
      }
    });
  } catch (error) {
    res.status(500).json({ error });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}\n`);
});
