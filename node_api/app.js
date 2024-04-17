#!/usr/bin/env node

const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const mysql = require('mysql');
const nodemailer = require('nodemailer');
const cors = require("cors");
const fs = require('fs');

// Middleware to parse JSON body
app.use(bodyParser.json());

app.use(cors()); // Cross origin enabled

// Route to handle signup
app.post("/signup", (req, res) => {

    try {
        if (!req.body.email || !req.body.first_name || !req.body.last_name) {
            res.status(400).json({ error: "Missing name or email"});
        }
        else {
            fetch("http://0.0.0.0:5000/api/v1/users", {
                headers: { 'Content-Type': 'application/json' },
                method: "POST",
                body: JSON.stringify(req.body)
            })
                .then(function(response) {
                    if (!response.ok) {
                        console.log("Signup failed");
                    }
                    return response.json();
                })
                .then(function(response) {
                    if (response.error) {
                        res.status(401).json({ error: response.error });
                    }
                    else {
                        let data = fs.readFileSync('confirmation_email.html', 'utf8');
                        data = data.replace(/{% id %}/g, `${response.id}`);
                        data = data.replace(/{% name %}/g, `${response.first_name} ${response.last_name}`);

                        const transporter = nodemailer.createTransport({
                            host: 'smtp-relay.brevo.com',
                            port: 587,
                            auth: {
                                user: process.argv[2],
                                pass: process.argv[3]
                            }
                        });
            
                        const mailOptions = {
                            from: 'mugabo@centralbees.com',
                            to: req.body.email,
                            subject: 'Welcome to Libly! Please comfim your email.',
                            text: data
                        };
            
                        transporter.sendMail(mailOptions, function (error, info) {
                            if (error) {
                                console.log(error);
                            } else {
                                console.log('Email sent: ' + info.response);
                            }
                        });

                        res.json({ success: "Sign up successful" });
                    }
                })
                .catch(error => {
                    res.json(error);
                });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Error reading HTML file' });
    }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}\n`);
});
