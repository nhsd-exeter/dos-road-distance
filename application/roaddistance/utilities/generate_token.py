import time
import bcrypt


secret = "Test string"
token_hash_sent = "$2y$04$jCIG/rZIgVS164GSm1wBY.JdOGoMzUA.0sEB79BMXoL0dplTtEcS2"


def check_authorisation_token(token_hash_sent: str) -> bool:
    time_factor = str(int(time.time() / 1800))
    print("Time window: " + time_factor)
    token = secret + time_factor
    salt = bcrypt.gensalt()
    token_encoded = str(bcrypt.hashpw(token.encode("utf-8"), salt))
    print("Secret: " + secret)
    print("Token sent: " + token_hash_sent)
    print("Token: " + token_encoded)
    return bcrypt.checkpw(token.encode("utf-8"), token_hash_sent.encode("utf-8"))


result = check_authorisation_token(token_hash_sent)
if result is True:
    print("Auth ok")
else:
    print("Forbidden")
