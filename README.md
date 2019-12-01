# Automation Arsenal

This repository is the codes I use personally to automate some workflow. Any PR to automate something is heavily appreciated! Please contact me if you find any issue.

## 1. Autosend gmail
prerequisite: set your google account's security level lower.
comming soon...

## 2. Automate the homework submittion on itc-lms(the system used in the University of Tokyo).
1. Install selenium, python-dotenv, and chromedriver. One possible way to install them is as follows:
```
pip install selenium python-dotenv
brew cask install chromedriver
```

2. Now chromedriver is installed in `/usr/local/bin/chromedriver`. Add `export PATH=$PATH:usr/local/bin` in your `.bash_profile`, `.zshrc` or whatever file according to your shell if you havn't.

3. touch `.env` and input your email address and password for itc-lms account. The sample `.env` file is at `.env.sample`.

4. Run the following command and it automatically uploads your homework to itc-lms!!
