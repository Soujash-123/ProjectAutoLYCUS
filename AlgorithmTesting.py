import csv
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

# Load data from CSV file
data = []
with open('encrypted_sentences.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        encrypted_string = row[2]
        string_length = row[3]
        encryption_name = row[4]
        data.append((encrypted_string, string_length, encryption_name))

# Prepare the training data
print(data)
X_train = [x[2] for x in data]
y_train = [x[1] for x in data]
# Vectorize the encrypted strings
print(X_train)
vectorizer = CountVectorizer(analyzer='char')
X_train_vectorized = vectorizer.fit_transform(X_train)

# Train the model
classifier = RandomForestClassifier(n_estimators=100)
classifier.fit(X_train_vectorized, y_train)

# Function to predict the encryption name for a given encrypted string
def predict_encryption_name(encrypted_string):
    # Vectorize the encrypted string
    X_test = [encrypted_string , len(encrypted_string)]
    X_test_vectorized = vectorizer.transform(X_test)
  
    # Make prediction
    predicted_encryption_name = classifier.predict(X_test_vectorized)[0]
    return predicted_encryption_name
score=0
negative=0
anomaly_data=[]
# Test the model manually
with open("testing.csv","r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        encrypted_string = row[2]
        encryption_name = row[4]
        for _ in range(100):
            predicted_name = predict_encryption_name(encrypted_string)
        
        if encryption_name == predicted_name:
            score+=1
        else:
            negative-=1
            print("Predicted encryption name:", predicted_name)
            print("Orignal encryption name:",encryption_name)
            anomaly_data.append(row)
with open("encrypted_sentences.csv","a",newline='') as file:
    writer=csv.writer(file)
    writer.writerows(anomaly_data)
print(anomaly_data)
print(score)
print(negative)
