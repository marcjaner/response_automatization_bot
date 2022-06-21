# Janer-Bus Bot
## Introduction
This project aims to create a telegram bot which handles booking and quote request reception, management and reply.

### Bot requirements

This bot should include the following functionalities:
- Get all not readed messages from the inbox
  - It should be able to differenciate whether a message is a booking or a quote request based on its subject
- Identify all important information and generate a summary of each email 
- Return a list with all summarized emails with an id to be able to select them
- Offer different possible replies:
  - `/yes` -> when a booking is accepted, this command will require a price and a booking number to identify each booking
    - An email to the client should be sended following the correct template filled with their personal information and the price and booking number provided with the command.
  - `/no` -> To reject a booking. An optional comment could be provided to be sent to the client if necessary. If not, a default rejection email will be sended. 
  - `/skip` -> If a booking needs to be processed manually this command should keep the message as an unread message
  - `/reply` -> In order to reply to a quote request, this command will require a price per transfer and a default email will be sended to the client.
- Detect the correct language and send an email using the correct html template based on the language and the type of email.
