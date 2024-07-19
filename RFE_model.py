import pandas as pd
from sklearn.feature_selection import RFE ,RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold,cross_validate
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score
import json
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score


def extract_features(data):
    features = []
    for item in data:
        if (item['severity'] == "CRITICAL" or item['severity'] == "MAJOR" or item['severity'] == "BLOCKER") and("javascript" in item['rule'] or "typescript" in item['rule']):
            feature = {
                "rule": item["rule"].split(":")[1],
                "severity": item["severity"],
                "effort": convert_to_minutes(item["effort"]),
                "debt": convert_to_minutes(item["debt"])
            }
            features.append(feature)
    return features


def convert_to_minutes(time_str):
    day = 0;
    hour = 0
    minutes= 0
    if 'd' in time_str:
        day_part = time_str.split('d')
        day = int(day_part[0])
        time_str = day_part[1] 

    if 'h' in time_str:
        hour_part = time_str.split('h')
        hour = int(hour_part[0])
        time_str = hour_part[1]  

    if 'min' in time_str:
        minutes = int(time_str.split('min')[0])

    total_minutes = day * 24 * 60 + hour * 60 + minutes
    return total_minutes   
 

def  RFE_model():
    total_data=[]
    with open('./RFE_total_code_smells.json', 'r', encoding='utf-8') as file:
        total_data = json.load(file)
    df = pd.DataFrame(total_data)

    # Convert 'severity' to binary target variable
    df['severity_binary'] = df['severity'].apply(lambda x: 1 if x == 'CRITICAL' else 0)
    df.drop(columns=['severity'], inplace=True)

    # Initialize LabelEncoder
    label_encoder = LabelEncoder()
    df['rule_encoded'] = label_encoder.fit_transform(df['rule'])


    X = df.drop(columns=['rule', 'severity_binary'])  
    y = df['severity_binary']  # Target 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


    model = LogisticRegression(max_iter=1000)
    n_features_to_select = min(10,X.shape[1])
    rfe = RFE(estimator=model, n_features_to_select=n_features_to_select)
    rfe.fit(X_train,y_train)

    feature_ranking = rfe.ranking_
    selected_features = X.columns[rfe.support_]

    print("Feature Ranking : ")
    for i, col in enumerate(X.columns):
         print(f"{col}: Rank {feature_ranking[i]}")

    

    rfe = RFE(estimator=model, n_features_to_select=20)  
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)

    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"\nPrecision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1}")

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

RFE_model()

