import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from codesmell_statistic import request_sonarQube, projects


def extract_features(data):
    features = []
    for item in data:
        if item['severity'] == "CRITICAL" or item['severity'] == "MAJOR":
            feature = {
                "rule": item["rule"],
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

 

def RFE_model():
    total_data = []
    for project in projects[0:3]:
        res = request_sonarQube(project['name'],project['key'])
        features = extract_features(res)
        total_data+=features

    df = pd.DataFrame(total_data)
    # One-Hot Encoding for 'rule'
    encoder = OneHotEncoder(sparse_output=False)
    encoded_rules = encoder.fit_transform(df[['rule']])

    #One-Hot Encoded set Column name
    encoded_rule_columns = encoder.get_feature_names_out(['rule'])
    encoded_df = pd.DataFrame(encoded_rules,columns=encoded_rule_columns)



    y = [1 if d["severity"]=="CRITICAL" else 0 for d in total_data]
    X = encoded_df
    
    model = LogisticRegression()

    n_features_to_select = min(10,X.shape[1])
    rfe = RFE(estimator=model, n_features_to_select=n_features_to_select)
    rfe.fit(X,y)

    feature_ranking = rfe.ranking_

    print("Feature Ranking : ")
    for i, col in enumerate(X.columns):
         print(f"{col}: Rank {feature_ranking[i]}")




RFE_model()

    
