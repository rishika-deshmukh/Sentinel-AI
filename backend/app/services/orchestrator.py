from sqlalchemy.orm import Session
from app.ml.generator import SyntheticDataGenerator
from app.ml.feature_pipeline import FeatureEngineeringPipeline
from app.ml.models import AnomalyDetectionEngine
from app.ml.explainer import ModelExplainer
from app.ml.game_engine import BayesianStackelbergGameEngine
from app.models.models import ThreatAnalysisRecord, Alert, Incident

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