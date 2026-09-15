import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

FEATURE_ORDER = [
    "login_hour",
    "files_accessed",
    "sensitive_files_accessed",
    "bytes_transferred_mb",
    "failed_logins",
    "privilege_level",
    "session_duration_min"
]

class FeatureEngineeringPipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        X = df[FEATURE_ORDER].fillna(0.0).values
        scaled_X = self.scaler.fit_transform(X)
        self.is_fitted = True
        return scaled_X

    def transform(self, df_or_dict) -> np.ndarray:
        if isinstance(df_or_dict, dict):
            df = pd.DataFrame([df_or_dict])
        else:
            df = df_or_dict
        
        for feature in FEATURE_ORDER:
            if feature not in df.columns:
                df[feature] = 0.0
                
        X = df[FEATURE_ORDER].fillna(0.0).values
        if not self.is_fitted:
            return X
        return self.scaler.transform(X)