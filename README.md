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

1. Clone the latest version of the repository
```bash
git clone https://github.com/unrealfar/zencipher
```

3. Install necessary packages
```bash
python3 -m pip install -r requirements.txt
```

4. Set up a database on MongoDB and get the MongoURI.

5. Create a public encryption using `cryptography.fernet`

6. Create an `os.env` file and fill in the following
```py
PUB_KEY="<Your public encryption key>"
MONGO_KEY="<Your MongoDB URI>"
SECRET_KEY="<A secret key for FastAPI(anything)>"
```

7. Run the code
```bash
python3 -m main
```

# Contact
- [@discord](https://discord.gg/PgYQZcBKQm)
- [@instagram](https://instagram.com/unrealfarrr)
