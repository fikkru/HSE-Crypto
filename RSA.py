import random
import math


def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Обратный элемент не существует")
    return x % phi


def generate_random_prime(start=100, end=300):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num


def generate_keys():
    p = generate_random_prime()
    q = generate_random_prime()
    while q == p:
        q = generate_random_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if e >= phi or gcd(e, phi) != 1:
        e = 3
        while e < phi:
            if gcd(e, phi) == 1:
                break
            e += 2

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)

    return p, q, public_key, private_key


def encrypt_bytes(data, public_key):
    e, n = public_key
    encrypted = [pow(byte, e, n) for byte in data]
    return encrypted


def decrypt_bytes(encrypted_data, private_key):
    d, n = private_key
    decrypted = bytes([pow(num, d, n) for num in encrypted_data])
    return decrypted


def save_public_key(filename, key):
    e, n = key
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{e}\n{n}\n")


def save_private_key(filename, key):
    d, n = key
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{d}\n{n}\n")


def load_key(filename):
    with open(filename, "r", encoding="utf-8") as f:
        a = int(f.readline().strip())
        n = int(f.readline().strip())
    return a, n


def encrypt_file(input_file, output_file, public_key):
    with open(input_file, "rb") as f:
        data = f.read()

    encrypted = encrypt_bytes(data, public_key)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(" ".join(map(str, encrypted)))

    print(f"Файл {input_file} зашифрован в {output_file}")


def decrypt_file(input_file, output_file, private_key):
    with open(input_file, "r", encoding="utf-8") as f:
        encrypted_data = list(map(int, f.read().split()))

    decrypted = decrypt_bytes(encrypted_data, private_key)

    with open(output_file, "wb") as f:
        f.write(decrypted)

    print(f"Файл {input_file} расшифрован в {output_file}")


def main():
    while True:
        print("\n--- RSA ---")
        print("1. Сгенерировать ключи")
        print("2. Зашифровать файл")
        print("3. Расшифровать файл")
        print("4. Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            p, q, public_key, private_key = generate_keys()
            print(f"Выбраны простые числа p={p}, q={q}")
            print(f"Открытый ключ: {public_key}")
            print(f"Закрытый ключ: {private_key}")

            save_public_key("public_key.txt", public_key)
            save_private_key("private_key.txt", private_key)
            print("Ключи сохранены в файлы public_key.txt и private_key.txt")

        elif choice == "2":
            input_file = input("Введите имя исходного файла: ")
            output_file = input("Введите имя файла для шифртекста: ")
            public_key = load_key("public_key.txt")
            encrypt_file(input_file, output_file, public_key)

        elif choice == "3":
            input_file = input("Введите имя зашифрованного файла: ")
            output_file = input("Введите имя файла для расшифрованных данных: ")
            private_key = load_key("private_key.txt")
            decrypt_file(input_file, output_file, private_key)

        elif choice == "4":
            print("Завершение работы.")
            break

        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()