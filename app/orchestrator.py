from typing import Dict, Optional

from app.tm1_templates import TM1TemplateFactory


def classify_question(question: str) -> str:
    q = question.lower().strip()

    if not q:
        return "clarification_needed"

    generation_signals = [
        "generate", "create", "build", "produce", "script", "process", "code",
        "ti process", "cube logic", "rule", "mdx", "chore", "tm1 process"
    ]
    impact_signals = [
        "impact", "affected", "what breaks", "change impact", "dependency",
        "ripple", "consequence", "risk", "dependency analysis"
    ]
    approach_signals = [
        "approach", "recommend", "best way", "solution design", "finalize",
        "option", "strategy", "design", "pattern", "how should we"
    ]

    if any(signal in q for signal in generation_signals):
        return "code_generation"
    if any(signal in q for signal in impact_signals):
        return "impact_analysis"
    if any(signal in q for signal in approach_signals):
        return "approach_finalization"

    return "clarification_needed"


def build_impact_summary(question: str) -> Optional[str]:
    lower = question.lower()
    impact_points = []

    if "cube" in lower:
        impact_points.append("Cube structure and data load behavior")
    if "dimension" in lower:
        impact_points.append("Dimension membership and hierarchy implications")
    if "process" in lower:
        impact_points.append("Process execution and dependency ordering")
    if "security" in lower or "access" in lower:
        impact_points.append("Security model and access control")
    if "performance" in lower or "speed" in lower:
        impact_points.append("Performance and memory overhead")

    if not impact_points:
        return None

    return "Impact review should include: " + "; ".join(impact_points) + "."


def build_recommended_approach(question: str) -> Optional[str]:
    lower = question.lower()

    if "dimension" in lower and "cube" in lower:
        return "Use a phased design: confirm dimension semantics, validate cube mappings, and test impacted processes before rollout."
    if "security" in lower or "access" in lower:
        return "Start with a security-impact review, define required roles, validate entitlement mappings, and then implement in a controlled release cycle."
    if "performance" in lower or "load" in lower:
        return "Prefer a minimal-change rollout with indexing, staging validation, and a controlled cutover window to measure performance impact."
    if "process" in lower or "ti" in lower:
        return "Standardize on a structured process pattern: source validation, staged load, reconciliation, and a rollback/monitoring checklist."

    return "Document assumptions, compare the viable options, validate dependencies, and choose the least risky implementation path."


def orchestrate_request(question: str) -> Dict[str, Optional[str]]:
    classification = classify_question(question)

    if classification == "code_generation":
        summary = "The request is to generate TM1 code."
        reasoning = "The user asked for code or automation, so the system should generate a TM1 artifact or procedural script."
        generated_code = TM1TemplateFactory.load_process_template("LoadData")
        return {
            "classification": classification,
            "output_type": "tm1_process",
            "summary": summary,
            "reasoning": reasoning,
            "generated_code": generated_code,
            "impact_summary": None,
            "recommended_approach": None,
        }

    if classification == "impact_analysis":
        summary = "The request is for impact analysis."
        reasoning = "The user is asking about effects, dependencies, or consequences, so a structured impact review is appropriate."
        return {
            "classification": classification,
            "output_type": "impact_analysis",
            "summary": summary,
            "reasoning": reasoning,
            "generated_code": None,
            "impact_summary": build_impact_summary(question),
            "recommended_approach": None,
        }

    if classification == "approach_finalization":
        summary = "The request needs an approach recommendation."
        reasoning = "The user is asking for a design or strategy recommendation, so the orchestrator should weigh options and finalize a path."
        return {
            "classification": classification,
            "output_type": "design_recommendation",
            "summary": summary,
            "reasoning": reasoning,
            "generated_code": None,
            "impact_summary": None,
            "recommended_approach": build_recommended_approach(question),
        }

    summary = "The request requires clarification before routing."
    reasoning = "The user question does not clearly indicate whether the need is code generation, impact analysis, or design evaluation."
    return {
        "classification": "clarification_needed",
        "output_type": "clarification",
        "summary": summary,
        "reasoning": reasoning,
        "generated_code": None,
        "impact_summary": None,
        "recommended_approach": "Ask the user to clarify the target TM1 object, expected outcome, and whether they need code, analysis, or design guidance.",
    }
