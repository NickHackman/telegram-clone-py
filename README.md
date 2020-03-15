# telegram-clone-py

[![Build Status](https://travis-ci.com/NickHackman/telegram-clone-py.svg?branch=master)](https://travis-ci.com/NickHackman/telegram-clone-py)

## Purpose

This Telegrram clone is written in Python for a computer science course at [Ohio
State Universiry](https://www.osu.edu/), CSE 3461. The purpose of
this clone is to satisfy the requirements of that project.

- Server and Client use `Sockets` to communicate via `TCP`
- Server must respond to a minimum of 5 different commands
- configuration file for port the server will listen on
- Server startup message
- Either prompt or use a configuration file to allow client to pick which server
  to connect to and port
- Server and Client work from 2 different IP addresses

| Assignment                            | Points |
| ------------------------------------- | ------ |
| Software submission                   | 75     |
| Demonstration / Review meeting        | 25     |
| **Bonus** Client-side GUI             | +2     |
| **Bonus** User Authorization          | +2     |
| **Bonus** Server-side command logging | +1     |
| Total                                 | 105    |

### Choices

Language: `Python`
Platform: Agnostic, but favoring `Linux/Unix`, depends on `GUI` library choice

## Goals

### Server

- Emulate [Flask](https://flask.palletsprojects.com/en/1.1.x/)\*
- Server uses a `REST`-esque API
- Emulate [Requests](https://2.python-requests.org/en/master/)\* for responses
- Sqlite3 database
- Allow multiple users
- All messages on Server are encrypted
- Use websockets to send and recieve messages from client

### Client

- Graphical User Interface (probably GTK or Qt)
- Emulate [Requests](https://2.python-requests.org/en/master/)\*
- Display chats with individual users
- Use private and public keys in order to keep messages private
- Function similarly to Telegram-desktop
- Allow `Markdown` in chat messages
- **Stretch Goal** send emoji

_\*_ But objectively **worse**

### Operations

- Create Account
- Edit Account
- Delete Account
- Send Message
- List Messages
- Edit Message
- Delete Message (only for everyone)
- List Users
