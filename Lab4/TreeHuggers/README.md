# Introduction

This README contains some notes to support Lab 4

## Viewing the openapi.json file

To view the openapi.json file, can easily do this by installing the VS Code "Live Server" extension. Search for "Live Server" in VS Code Extensions. It is authored by Ritwick Dey

Then right-click the swagger.html file and select Open with Live Server

This will automatically open your browser on http://127.0.0.1:5500/swagger.html

If you are not using VS Code, other ways to view this file are:

1. Use Python e.g. in a terminal enter `python3 -m http.server 8000` and then open http://localhost:8000/swagger.html
2. via Node http-server, firstly run `npm install -g http-server` to install it. Then `http-server .`

## Optional packages

Other helpful packages you may want to install are:

* SonarQube for IDE - helps check code quality when editing code. Works for many languages, not just Python
* PyLance - helpful plugin for helping to write good Python code