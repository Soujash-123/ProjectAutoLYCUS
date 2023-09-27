import csv
import random
from Crypto.Cipher import AES, DES, ARC4
from Crypto.Util.Padding import pad
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier


class AutoLYCUS:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.vectorizer = CountVectorizer(analyzer='char')
        self.classifier = RandomForestClassifier(n_estimators=100)
        self.load_data()

    def generate_random_sentence(self):
        words = ['apple', 'banana', 'cat', 'dog', 'elephant', 'fox', 'gorilla', 'horse', 'iguana', 'jaguar']
        sentence = ' '.join(random.choices(words, k=random.randint(3, 8)))
        return sentence

    def encrypt_aes(self, plaintext, key):
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return ciphertext.hex()

    def encrypt_des(self, plaintext, key):
        cipher = DES.new(key, DES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), DES.block_size))
        return ciphertext.hex()

    def encrypt_arc4(self, plaintext, key):
        cipher = ARC4.new(key)
        ciphertext = cipher.encrypt(plaintext.encode())
        return ciphertext.hex()

    def generate_encrypted_sentences(self):
        encryption_algorithms = [
            {'name': 'AES', 'function': self.encrypt_aes},
            {'name': 'DES', 'function': self.encrypt_des},
            {'name': 'ARC4', 'function': self.encrypt_arc4}
        ]

        data = []
        for _ in range(1):
            sentence = self.generate_random_sentence()
            key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=16)).encode()
            for algorithm in encryption_algorithms:
                encrypted_string = algorithm['function'](sentence, key)
                data.append([sentence, key.decode(), encrypted_string, len(encrypted_string), algorithm['name']])
        return data

    def store_data_to_csv(self):
        data = self.generate_encrypted_sentences()
        with open(self.file_path, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print("Data Writing Completed")

    def load_data(self):
        with open(self.file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                encrypted_string = row[2]
                string_length = int(row[3])
                encryption_name = row[4]
                self.data.append((encrypted_string, string_length, encryption_name))

    def train_model(self):
        X_train = [x[0] for x in self.data]
        y_train = [x[2] for x in self.data]
        X_train_vectorized = self.vectorizer.fit_transform([x[0] + str(x[1]) for x in self.data])
        self.classifier.fit(X_train_vectorized, y_train)

    def predict_encryption_name(self, encrypted_string):
        X_test = [encrypted_string]
        X_test_vectorized = self.vectorizer.transform(X_test)
        predicted_name = self.classifier.predict(X_test_vectorized)[0]
        return predicted_name

    def find_most_probable(self, lst):
        encryption_stds = ["AES", "DES", "ARC4"]
        count = {}
        for i in encryption_stds:
            count[lst.count(i)] = i
        probable_order = [count[i] for i in sorted(count.keys(), reverse=True)]
        return probable_order, count


# Usage:
if __name__ == '__main__':
    auto_lycus = AutoLYCUS('encrypted_sentences.csv')
    # auto_lycus.store_data_to_csv()
    auto_lycus.load_data()
    encrypted_string = input("Enter an encrypted string: ")
    probable_name = []
    for _ in range(100):
        auto_lycus.train_model()
        probable_name.append(auto_lycus.predict_encryption_name(encrypted_string))
    predicted_name, count = auto_lycus.find_most_probable(probable_name)
    # predicted_name = auto_lycus.predict_encryption_name(encrypted_string)
    print("Possibilities:")
    for i in count:
        print(i, "%:", count[i])
    print(predicted_name)
    print("Most probable:", predicted_name[0])
