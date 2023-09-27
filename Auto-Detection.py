import csv
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

class AutoLYCUS:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []
        self.vectorizer = CountVectorizer(analyzer='char')
        self.classifier = RandomForestClassifier(n_estimators=100)
        self.load_data()
    
    def load_data(self):
        with open(self.file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                encrypted_string = row[2]
                encryption_name = row[4]
                self.data.append((encrypted_string, encryption_name))
    
    def train_model(self):
        X_train = [x[0] for x in self.data]
        y_train = [x[1] for x in self.data]
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
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
        return probable_order

# Usage:
if __name__ == '__main__':
    auto_lycus = AutoLYCUS('encrypted_sentences.csv')
    auto_lycus.train_model()
    encrypted_string = input("Enter an encrypted string: ")
    predicted_name = auto_lycus.predict_encryption_name(encrypted_string)
    print("Predicted encryption name:", predicted_name)
