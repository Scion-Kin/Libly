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
            console.log("Missing details");
            res.status(400).json({ error: "Missing name or email"});
        }
        else {
            let data = fs.readFileSync('confirmation_email.html', 'utf8');
            data = data.replace(/{% email %}/g, `${req.body.email}`);
            data = data.replace(/{% name %}/g, `${req.body.first_name} ${req.body.last_name}`);

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
                        res.status(401).json({ error: "email already exists" });
                    }
                    else {
                        const transporter = nodemailer.createTransport({
                            host: 'smtp-relay.brevo.com',
                            port: 587,
                            auth: {
                                user: 'dinturner17@gmail.com',
                                pass: 'HzSB6UdyCMbsGwAX'
                            }
                        });
            
                        const mailOptions = {
                            from: 'mugabo@centralbees.com',
                            to: req.body.email,
                            subject: 'Welcome to Libly! Email confirmation needed',
                            text: data
                        };
            
                        transporter.sendMail(mailOptions, function (error, info) {
                            if (error) {
                                console.log(error);
                            } else {
                                console.log('Email sent: ' + info.response);
                            }
                        });

                        res.json({ success: "Signup successfull!"});
                    }
                })
                .catch(error => {
                    res.json(error);
                });
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('Error reading HTML file');
    }
});

app.post("/login", (req, res) => {

    const con = mysql.createConnection({
        host: "localhost",
        user: "libly_user",
        password: "libDev",
        database: "libly"
    });
      
    con.connect(function(err) {
      if (err) throw err;
      con.query(`SELECT * FROM users WHERE email = '${req.body.email}'`, function (err, result, fields) {
        if (err) {
          res.json(err);
        }
        else {
          if (result[0].password != req.body.password) {
            res.status(401).json({ error: "Wrong credentials" });
          }
          else {
            res.json({ success: "Login successful", user_details: result[0]});
          }
        }
      });
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}\n`);
});
