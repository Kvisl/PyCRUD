import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS Phone_numbers(
            number VARCHAR(20) NOT NULL UNIQUE,
            id_client INT NOT NULL REFERENCES Clients(id)
        );
        ''')
    conn.commit()


def add_client(conn, first_name, last_name, email, number=None):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO Clients(first_name, last_name, email)
            VALUES (%s, %s, %s)
            RETURNING id, first_name, last_name, email;
        ''', (first_name, last_name, email,))
        insert_client = cur.fetchone()
        return insert_client


def add_phone_number(conn, id_client, number):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO Phone_numbers(number, id_client)
            VALUES(%s, %s)
            RETURNING id_client, number;
        ''', (number, id_client,))
        insert_phone = cur.fetchone()
        return insert_phone


def change_client(conn, id_client, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE Clients
            SET first_name=%s, last_name=%s, email=%s
            WHERE id=%s
            RETURNING id, first_name, last_name, email;
        ''', (first_name, last_name, email, id_client,))
        update_client = cur.fetchone()
        return update_client


def change_phone(conn, id_client, number):
    with conn.cursor() as cur:
        cur.execute('''
        UPDATE phone_numbers
            SET  number=%s
            WHERE id_client=%s
            RETURNING id_client, number;
        ''', (number, id_client,))
        update_phone = cur.fetchone()
        return update_phone


def delete_phone(conn, id_client, number):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM Phone_numbers
            WHERE id_client=%s
            RETURNING id_client, number;
        ''', (id_client,))
        delete = cur.fetchone()
        return delete


def delete_client(conn, id):
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM Clients
            WHERE id=%s
            RETURNING id;
        ''', (id,))
        delete = cur.fetchone()
        return delete


def find_client(conn, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT Clients.first_name, Clients.last_name, Clients.email
           FROM Clients
           LEFT JOIN Phone_numbers ON Clients.id = Phone_numbers.id_client
           WHERE first_name=%s OR last_name=%s OR email=%s OR number=%s;
        ''', (first_name, last_name, email, number,))
        select_client = cur.fetchone()
        return select_client


with psycopg2.connect(database="clients", user="postgres", password="530496", host='localhost', port='5432') as conn:
    create_db(conn)
    print(add_client(conn, 'Ivan', 'Petrov', 'ivan@mail.ru'))
    print(add_phone_number(conn, 1, '+78881234567'))
    print(change_client(conn, 1, 'Pavel', 'Ivanov', 'pavel@gmail.com'))
    print(change_phone(conn, 1, '+75550987654'))
    print(delete_phone(conn, 1, '+77750987654'))
    print(delete_client(conn, 1))
    print(find_client(conn, first_name='', last_name='',  email='ivan@mail.ru', number=''))
