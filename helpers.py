def hash(password):
    # discard repeated values
    password = set(password)
    # initialize variable to store all ord() chracters
    int_pool = 1
    # initialize list to append the final hash char
    hash_plain = []

    for i in password:
        int_pool *= ord(i)

    int_pool **= 100
    pool_str = str(int_pool)

    for i in range(4, 81):
        if i % 4 == 0:
            number = int(pool_str[:i])
            number_table = number % 127

            if number_table < 32:
                number_table += 32

            char_number = chr(number_table)
            hash_plain.append(char_number)

    return "".join(hash_plain)


def check_password_hash(hash_db, password):
    if hash(password) == hash_db:
        return True
    return False
