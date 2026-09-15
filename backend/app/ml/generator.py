import numpy as np
import pandas as pd

class SyntheticDataGenerator:
    """
    Generates synthetic corporate enterprise access logs
    modeling Normal users and Malicious Insider Threat activities.
    """
    def __init__(self, seed: int = 42):
        np.random.seed(seed)

    def generate_baseline_dataset(self, n_samples: int = 1200) -> pd.DataFrame:
        n_normal = int(n_samples * 0.90)
        n_malicious = n_samples - n_normal

        # Normal activity profile
        normal_data = {
            "login_hour": np.random.normal(loc=11, scale=2.5, size=n_normal).clip(8, 18),
            "files_accessed": np.random.poisson(lam=12, size=n_normal).clip(1, 40),
            "sensitive_files_accessed": np.random.binomial(n=5, p=0.08, size=n_normal),
            "bytes_transferred_mb": np.random.exponential(scale=15.0, size=n_normal).clip(0.1, 120),
            "failed_logins": np.random.binomial(n=3, p=0.05, size=n_normal),
            "privilege_level": np.random.choice([0, 1], size=n_normal, p=[0.85, 0.15]),
            "session_duration_min": np.random.normal(loc=180, scale=45, size=n_normal).clip(10, 480),
            "label": 0  # Normal
        }

        # Malicious profile: Data Exfiltration & Off-hour Reconnaissance
        malicious_data = {
            "login_hour": np.concatenate([
                np.random.uniform(0, 5, size=n_malicious // 2),
                np.random.uniform(20, 23, size=n_malicious - (n_malicious // 2))
            ]),
            "files_accessed": np.random.poisson(lam=65, size=n_malicious).clip(20, 180),
            "sensitive_files_accessed": np.random.poisson(lam=14, size=n_malicious).clip(3, 40),
            "bytes_transferred_mb": np.random.normal(loc=1250, scale=350, size=n_malicious).clip(400, 3500),
            "failed_logins": np.random.poisson(lam=4, size=n_malicious).clip(1, 10),
            "privilege_level": np.random.choice([1, 2], size=n_malicious, p=[0.4, 0.6]),
            "session_duration_min": np.random.normal(loc=420, scale=60, size=n_malicious).clip(60, 720),
            "label": 1  # Malicious Insider
        }

        df_normal = pd.DataFrame(normal_data)
        df_malicious = pd.DataFrame(malicious_data)
        df_combined = pd.concat([df_normal, df_malicious], ignore_index=True)
        return df_combined.sample(frac=1.0, random_state=42).reset_index(drop=True)

    def simulate_adaptive_sample(self, evasion_level: float = 0.0) -> dict:
        """
        Generates telemetry for an attacker adapting to detection:
        evasion_level = 0.0 (aggressive exfiltration) -> 1.0 (stealthy low-and-slow)
        """
        transfer = (1.0 - evasion_level) * 1500.0 + evasion_level * 60.0
        sensitive = int((1.0 - evasion_level) * 18 + evasion_level * 2)
        hour = 2 if evasion_level < 0.5 else 14
        
        return {
            "login_hour": float(hour),
            "files_accessed": float(int((1.0 - evasion_level) * 75 + evasion_level * 15)),
            "sensitive_files_accessed": float(sensitive),
            "bytes_transferred_mb": float(transfer),
            "failed_logins": float(0 if evasion_level > 0.4 else 3),
            "privilege_level": float(1 if evasion_level > 0.6 else 2),
            "session_duration_min": float(220 if evasion_level > 0.5 else 480)
        }