import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM

class AnomalyDetectionEngine:
    def __init__(self):
        self.iforest = IsolationForest(
            n_estimators=100,
            contamination=0.10,
            random_state=42
        )
        self.ocsvm = OneClassSVM(
            kernel="rbf",
            gamma="scale",
            nu=0.10
        )
        self.is_trained = False

    def train(self, X_train: np.ndarray):
        self.iforest.fit(X_train)
        self.ocsvm.fit(X_train)
        self.is_trained = True

    def evaluate(self, X: np.ndarray):
        if not self.is_trained:
            raise RuntimeError("Anomaly models must be trained before evaluation.")
        
        # Decision function: lower scores indicate higher anomalousness
        if_raw = self.iforest.decision_function(X)
        oc_raw = self.ocsvm.decision_function(X)
        
        if_pred = self.iforest.predict(X)  # -1 = anomaly, 1 = normal
        oc_pred = self.ocsvm.predict(X)

        return {
            "iforest_score": float(if_raw[0]),
            "ocsvm_score": float(oc_raw[0]),
            "iforest_anomaly": bool(if_pred[0] == -1),
            "ocsvm_anomaly": bool(oc_pred[0] == -1)
        }

    @staticmethod
    def compute_risk_score(if_score: float, oc_score: float, raw_features: dict) -> float:
        """
        Maps model anomaly margins and high-weight security metrics to a 0-100 risk score.
        """
        # Invert and normalize typical decision outputs (approx range -0.3 to +0.3)
        if_component = np.clip((0.25 - if_score) / 0.50, 0.0, 1.0) * 40.0
        oc_component = np.clip((0.25 - oc_score) / 0.50, 0.0, 1.0) * 30.0

        # Heuristic security penalties based on critical enterprise exfiltration indicators
        penalties = 0.0
        if raw_features.get("bytes_transferred_mb", 0) > 300:
            penalties += 15.0
        if raw_features.get("sensitive_files_accessed", 0) >= 5:
            penalties += 10.0
        if raw_features.get("login_hour", 12) < 6 or raw_features.get("login_hour", 12) > 21:
            penalties += 5.0

        final_score = float(np.clip(if_component + oc_component + penalties, 0.0, 100.0))
        return round(final_score, 2)