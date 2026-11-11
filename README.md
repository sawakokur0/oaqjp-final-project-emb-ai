# Final Project

A Flask web application that uses IBM Watson NLP to score anger, disgust,
fear, joy, and sadness in English text and identify the dominant emotion.

Install Flask and Requests, then run `python3 server.py` and open
`http://localhost:5000`. Live predictions require access to the Watson NLP
service from IBM Skills Network. The unit tests use deterministic fixtures.

Run the tests with `python3 -m unittest -v`.
