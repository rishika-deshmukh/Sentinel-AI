from sqlalchemy.orm import Session
from datetime import datetime

from app.ml.generator import SyntheticDataGenerator
from app.ml.feature_pipeline import FeatureEngineeringPipeline
from app.ml.models import AnomalyDetectionEngine
from app.ml.explainer import ModelExplainer
from app.ml.game_engine import BayesianStackelbergGameEngine
from app.models.models import ThreatAnalysisRecord, Alert, Incident, SecureAuditLog

# Import Stage 8 ML-DSA Engine
from app.core.pqc_dsa import dsa_engine

class SentinelOrchestrator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SentinelOrchestrator, cls).__new__(cls)
            cls._instance.initialize_pipeline()
        return cls._instance

    def initialize_pipeline(self):
        self.generator = SyntheticDataGenerator(seed=42)
        self.feature_pipeline = FeatureEngineeringPipeline()
        self.ml_engine = AnomalyDetectionEngine()
        self.game_engine = BayesianStackelbergGameEngine()

        # Bootstrap training with synthetic baseline
        df_train = self.generator.generate_baseline_dataset(n_samples=1000)
        X_train_scaled = self.feature_pipeline.fit_transform(df_train)
        self.ml_engine.train(X_train_scaled)
        self.explainer = ModelExplainer(self.ml_engine.iforest, X_train_scaled)

    def analyze_event(self, user_id: int, raw_features: dict, db: Session) -> dict:
        # 1. Feature Transformation
        scaled_sample = self.feature_pipeline.transform(raw_features)

        # 2. Dual-Model Anomaly Detection
        eval_results = self.ml_engine.evaluate(scaled_sample)

        # 3. Normalized Risk Scoring
        risk_score = self.ml_engine.compute_risk_score(
            eval_results["iforest_score"],
            eval_results["ocsvm_score"],
            raw_features
        )

        # 4. SHAP Feature Attribution
        shap_scores = self.explainer.explain(scaled_sample)

        # 5. Game-Theoretic Stackelberg Response Strategy
        game_decision = self.game_engine.resolve_optimal_defense(risk_score)
        action = game_decision["selected_action"]

        # 6. Persistent Threat Record
        threat_record = ThreatAnalysisRecord(
            user_id=user_id,
            raw_features=raw_features,
            iforest_score=eval_results["iforest_score"],
            ocsvm_score=eval_results["ocsvm_score"],
            risk_score=risk_score,
            shap_attributions=shap_scores,
            game_action=action,
            attacker_state="ADAPTIVE_ACTIVE" if risk_score > 60 else "BENIGN"
        )
        db.add(threat_record)

        # 7. Automated Alert & Incident Triggering
        if risk_score >= 50.0:
            alert = Alert(
                user_id=user_id,
                severity="CRITICAL" if risk_score > 80 else "HIGH" if risk_score > 65 else "MEDIUM",
                risk_score=risk_score,
                triggering_factors=shap_scores,
                recommended_action=action
            )
            db.add(alert)

        if risk_score >= 75.0:
            incident = Incident(
                title=f"Automated Alert: High-Risk Exfiltration Detected for User {user_id}",
                user_id=user_id,
                risk_score=risk_score,
                shap_summary=shap_scores,
                enforced_action=action,
                status="OPEN"
            )
            db.add(incident)

        # =====================================================================
        # STAGE 8: TAMPER-EVIDENT CRYPTOGRAPHIC AUDIT LOGGING (ML-DSA)
        # =====================================================================
        try:
            # 1. Fetch the previous signature to continue the chain
            last_log = db.query(SecureAuditLog).order_by(SecureAuditLog.id.desc()).first()
            previous_signature = last_log.cryptographic_hash if last_log else dsa_engine.genesis_hash

            # 2. Package the exact decision details
            event_payload = {
                "user_id": user_id,
                "risk_score": float(risk_score),
                "game_action": action,
                "timestamp": str(datetime.utcnow())
            }

            # 3. Create the quantum-secure digital signature
            new_signature = dsa_engine.sign_incident(
                incident_data=event_payload, 
                previous_signature=previous_signature
            )

            # 4. Save the chained seal to the database
            secure_log = SecureAuditLog(
                event_payload=event_payload,
                cryptographic_hash=new_signature,
                previous_hash=previous_signature
            )
            db.add(secure_log)
            
            print(f"\n[STAGE 8 ACTIVE] ML-DSA-65 Digital Wax Seal Applied.")
            print(f" -> Chained to Previous: {previous_signature[:20]}...")
            print(f" -> New Block Seal: {new_signature[:20]}...\n")
            
        except Exception as e:
            print(f"[STAGE 8 ERROR] Failed to seal ledger: {e}")
        # =====================================================================

        # Commit everything (Alerts, Incidents, and the Secure Audit Log) at once
        db.commit()

        return {
            "user_id": user_id,
            "risk_score": risk_score,
            "iforest_anomaly": eval_results["iforest_anomaly"],
            "ocsvm_anomaly": eval_results["ocsvm_anomaly"],
            "game_action": action,
            "top_explanations": shap_scores,
            "details": {
                "decision_distribution": game_decision["action_distribution"],
                "utility": game_decision["expected_utility"],
                "iforest_metric": eval_results["iforest_score"],
                "ocsvm_metric": eval_results["ocsvm_score"]
            }
        }

orchestrator = SentinelOrchestrator()