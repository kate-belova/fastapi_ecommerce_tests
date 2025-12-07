from faker import Faker

random_generator = Faker()

valid_user_data = [
    {
        'email': random_generator.email(),
        'password': random_generator.password(length=8),
    },
    {
        'email': random_generator.email(),
        'password': random_generator.password(length=9),
        'role': 'seller',
    },
    {
        'email': random_generator.email(),
        'password': random_generator.password(length=15),
        'role': 'buyer',
    },
]

invalid_user_data = [
    {'email': '', 'password': ''},
    {
        'email': 'invalid-email.ru',
        'password': random_generator.password(length=8),
    },
    {
        'email': 'invalid-email@gmail',
        'password': random_generator.password(length=10),
        'role': 'seller',
    },
    {
        'email': 'invalid-email@yandex.',
        'password': random_generator.password(length=12),
        'role': 'buyer',
    },
    {
        'email': random_generator.email(),
        'password': '',
        'role': 'seller',
    },
    {
        'email': random_generator.email(),
        'password': random_generator.password(length=7),
        'role': 'seller',
    },
    {
        'email': random_generator.email(),
        'password': random_generator.password(length=7),
        'role': '',
    },
    {
        'email': random_generator.email(),
        'password': random_generator.password(length=7),
        'role': 'admin',
    },
]

invalid_auth_data = [
    {
        'username': random_generator.email(),
        'password': random_generator.password(length=8),
    },
    {
        'username': 'laptops-seller@ecommerce-db.com',
        'password': random_generator.password(length=10),
    },
    {'username': random_generator.email(), 'password': 'a1ex_the_best'},
    {'username': '', 'password': ''},
]

invalid_refresh_token = ['', 'invalid_refresh_token']
