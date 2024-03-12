# Password Manager

## Overview:

A simple command-line application to store and retrieve passwords. The passwords will be stored in AWS Secrets Manager. Accessing the AWS account with Access Key ID and Secret Key is considered sufficient authorisation to retrieve the passwords.

The application allows you to:

- store a user id and password in `secretsmanager`
- list all the stored secrets
- retrieve a secret - the resulting user ID and password will be stored in a file, not printed
- delete a secret
