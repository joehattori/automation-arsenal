# Automation Arsenal

This repository is the codes I use personally to automate some workflow. Any PR to automate something is heavily appreciated! Please contact me if you find any issue.

## 1. Autosend gmail
prerequisite: set your google account's security level lower.
comming soon...

## 2. Automate the homework submittion on itc-lms(a website used in the University of Tokyo).
- Install selenium, python-dotenv, and chromedriver. One possible way to install them is as follows:

```
$ pip install selenium python-dotenv
$ brew cask install chromedriver
```

- Now chromedriver is installed in `/usr/local/bin/chromedriver`. Add `export PATH=$PATH:usr/local/bin` in your `.bash_profile`, `.zshrc` or whatever file according to your shell if you haven't.

- Touch `.env` and input your email address and password for itc-lms account. The sample `.env` file is at `.env.sample`.

- Run the following command and it automatically uploads your homework to itc-lms!!

## 3. Download file from Dropbox
1. Run `npm i -D`.
2. Set Dropbox App's access token.
3. `node dropbox.js [filename]` will download the file into your directory.
