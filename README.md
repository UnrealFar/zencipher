# ZenCipher
> Secure platform to store all your passwords

# Features
- Double-layer encryption
- Easy to use
- Open-sourced

# Contribute to ZenCipher
> Feel free to make pull requests and issues to contribute to the development of our project.
> Contact me for collaborations or to give suggestions at [Contact](#Contact)

# Create your own instance

- Set up the instance
```bash
# Clone the repository
git clone https://github.com/unrealfar/zencipher

cd .

# Install the requirements
python3 -m pip install -r requirements.txt
```

- Set up a database on MongoDB and get the MongoURI.
- Create a public encryption using `cryptography.fernet`

- Create an `os.env` file and fill in the following
```py
PUB_KEY="<Your public encryption key>"
MONGO_KEY="<Your MongoDB URI>"
SECRET_KEY="<A secret key for FastAPI(anything)>"
```

- Run the code
```bash
python3 -m main
```

> Your ZenCipher instance is ready for use.

# Contact
- [@github](https://github.com/unrealfar)
- [@discord](https://discord.gg/PgYQZcBKQm)
- [@instagram](https://instagram.com/unrealfarrr)
