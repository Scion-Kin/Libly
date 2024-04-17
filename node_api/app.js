#!/usr/bin/env node

const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const mysql = require('mysql');
const nodemailer = require('nodemailer');
const cors = require("cors");

// Middleware to parse JSON body
app.use(bodyParser.json());

app.use(cors()); // Cross origin enabled

// Route to handle signup
app.post("/signup", (req, res) => {

    const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'gridofthis@gmail.com',
            pass: 'MyNigga'
        }
    });

    const mailOptions = {
        from: 'gridofthis@gmail.com',
        to: req.body.email,
        subject: 'Welcome to Libly',
        text: 'Enjoy reading on Libly!'
    };

    transporter.sendMail(mailOptions, function (error, info) {
        if (error) {
            console.log(error);
        } else {
            console.log('Email sent: ' + info.response);   

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
                .then(function(data) {
                    if (data.error) {
                        res.status(401).json({ error: "email already exists" });
                    }
                    else {

                        res.json({ success: "Signup successfull!"});
                    }
                })
                .catch(error => {
                res.json(error);
                });
        }
    }); 
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
            res.json({ success: "Login successful"});
          }
        }
      });
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
