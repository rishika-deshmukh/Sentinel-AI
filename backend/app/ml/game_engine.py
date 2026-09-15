import numpy as np
from scipy.optimize import linprog

class BayesianStackelbergGameEngine:
    """
    Solves an Adaptive Bayesian Stackelberg Security Game:
    Leader (Defender): SentinelAI Orchestrator choosing enforcement actions
    Follower (Attacker): Insider choosing exfiltration strategy
    Payoffs are parameterized by real-time risk scores and observed telemetry.
    """
    ACTIONS = ["ALLOW", "MONITOR", "STEP_UP_AUTH", "RESTRICT", "REVOKE"]
    ATTACKER_STRATEGIES = ["STEALTH_EXFILTRATION", "RAPID_EXFILTRATION", "ABORT"]

    def __init__(self):
        # Defender payoff matrix: [Defender Action x Attacker Strategy]
        # Higher values represent higher utility for the defender
        self.base_defender_payoffs = np.array([
            [ 2.0, -10.0,  5.0],   # ALLOW
            [ 4.0,  -4.0,  3.0],   # MONITOR
            [ 3.0,   1.0,  1.0],   # STEP_UP_AUTH
            [ 1.0,   6.0, -1.0],   # RESTRICT
            [-2.0,   9.0, -4.0]    # REVOKE (high penalty if abort/normal)
        ])

    def resolve_optimal_defense(self, risk_score: float, adaptive_modifier: float = 0.0) -> dict:
        """
        Dynamically adjusts payoffs using the measured risk score,
        then evaluates the Stackelberg Leader decision.
        """
        # Dynamic payoff weighting based on risk magnitude
        adjusted_payoffs = self.base_defender_payoffs.copy()
        risk_norm = risk_score / 100.0

        # Adjust defender urgency based on risk
        adjusted_payoffs[0] -= risk_norm * 12.0  # Cost of ALLOW surges
        adjusted_payoffs[1] -= risk_norm * 4.0
        adjusted_payoffs[3] += risk_norm * 8.0   # Utility of RESTRICT increases
        adjusted_payoffs[4] += risk_norm * 14.0  # Utility of REVOKE increases

        # Determine best pure response via minimax mixed-strategy boundary
        # Linear programming solver for zero-sum / Stackelberg approximation
        num_actions = len(self.ACTIONS)
        c = np.zeros(num_actions + 1)
        c[-1] = -1.0  # Maximize utility scalar v

        # Constraints: - A^T * p + v <= 0
        A_ub = np.hstack([-adjusted_payoffs.T, np.ones((len(self.ATTACKER_STRATEGIES), 1))])
        b_ub = np.zeros(len(self.ATTACKER_STRATEGIES))

        # Probability simplex constraints sum(p) == 1
        A_eq = np.array([[1.0] * num_actions + [0.0]])
        b_eq = [1.0]
        bounds = [(0, 1) for _ in range(num_actions)] + [(None, None)]

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

        if res.success:
            probabilities = res.x[:num_actions]
            probabilities = np.maximum(probabilities, 0)
            probabilities /= probabilities.sum()
            chosen_action_idx = int(np.argmax(probabilities))
        else:
            # Fallback deterministic partition
            if risk_score < 30:
                chosen_action_idx = 0
            elif risk_score < 55:
                chosen_action_idx = 1
            elif risk_score < 75:
                chosen_action_idx = 2
            elif risk_score < 90:
                chosen_action_idx = 3
            else:
                chosen_action_idx = 4
            probabilities = np.zeros(num_actions)
            probabilities[chosen_action_idx] = 1.0

        return {
            "selected_action": self.ACTIONS[chosen_action_idx],
            "action_distribution": {self.ACTIONS[i]: round(float(probabilities[i]), 4) for i in range(num_actions)},
            "expected_utility": round(float(res.fun * -1 if res.success else 0.0), 3)
        }