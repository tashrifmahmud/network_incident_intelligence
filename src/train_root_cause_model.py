import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def train_model():
    df = pd.read_csv("data/incident_features.csv")

    # Columns we do NOT want as model inputs
    drop_columns = [
        "incident_id",
        "incident_start_time",
        "incident_end_time",
        "site_id",
        "service_id",
        "root_cause",
        "ticket_status",
    ]

    X = df.drop(columns=drop_columns)
    y = df["root_cause"]

    # One-hot encode remaining text columns
    X = pd.get_dummies(X, columns=["region", "priority"], drop_first=False)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        max_depth=10
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("\nRoot Cause Classification Results")
    print("-" * 40)
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    feature_importance = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    print("\nTop 15 Important Features:")
    print(feature_importance.head(15).to_string(index=False))
    
        # Save model
    joblib.dump(model, "data/root_cause_model.pkl")
    joblib.dump(X.columns.tolist(), "data/model_features.pkl")

    print("\nModel saved:")
    print("data/root_cause_model.pkl")


if __name__ == "__main__":
    train_model()
