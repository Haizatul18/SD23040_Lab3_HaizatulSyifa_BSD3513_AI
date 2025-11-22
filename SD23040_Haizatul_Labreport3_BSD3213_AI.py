import streamlit as st
import json

st.title("Scholarship Advisory Rule-Based System")
st.write("### BSD3513 – Lab Report 3")
st.write("This decision support tool uses a rule-based engine to determine scholarship eligibility.")
st.image("scholarship_opportunity.jpg", caption="Scholarship Opportunity", use_container_width=True)


DEFAULT_RULES = [
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]

# ============================
# DISPLAY RULES JSON (Editable)
# ============================

rules_json = st.text_area(
    "Scholarship Rules (DO NOT MODIFY STRUCTURE)",
    json.dumps(DEFAULT_RULES, indent=4),
    height=400
)

# Optional: hide rules inside expander
with st.expander("View Scholarship Rules (Optional)"):
    st.json(DEFAULT_RULES)

# ============================
# APPLICANT INFORMATION FORM
# ============================

st.header("Applicant Information")

col1, col2 = st.columns(2)

with col1:
    cgpa = st.number_input("CGPA", min_value=0.00, max_value=4.00, step=0.01)
    co_score = st.slider("Co-Curricular Score (0–100)", 0, 100, 50)

with col2:
    family_income = st.slider("Monthly Family Income (RM)", 0, 20000, 3000, step=100)
    discipline = st.number_input("Number of Disciplinary Actions", min_value=0, max_value=10)

service = st.number_input("Community Service Hours", min_value=0)
semester = st.number_input("Current Semester", min_value=1, max_value=12)

# ============================
# RULE EVALUATION FUNCTION
# ============================

def evaluate_rules(rules, facts):
    valid_rules = []
    for rule in rules:
        is_valid = True
        for cond in rule["conditions"]:
            field, op, value = cond
            user_val = facts[field]

            if op == ">=" and not (user_val >= value): is_valid = False
            if op == "<=" and not (user_val <= value): is_valid = False
            if op == ">" and not (user_val > value): is_valid = False
            if op == "<" and not (user_val < value): is_valid = False
            if op == "==" and not (user_val == value): is_valid = False

        if is_valid:
            valid_rules.append(rule)

    # Sort by priority (higher wins)
    valid_rules.sort(key=lambda r: r["priority"], reverse=True)
    return valid_rules[0] if valid_rules else None

# ============================
# SUBMIT & RESULT PROCESSING
# ============================

if st.button("Evaluate Scholarship Eligibility"):

    rules = json.loads(rules_json)

    facts = {
        "cgpa": cgpa,
        "family_income": family_income,
        "co_curricular_score": co_score,
        "community_service": service,
        "semester": semester,
        "disciplinary_actions": discipline
    }

    result = evaluate_rules(rules, facts)

    if result:
        st.success(f"Decision: **{result['action']['decision']}**")
        st.write(f"Reason: {result['action']['reason']}")
        st.write(f"Rule Matched: **{result['name']}** (Priority {result['priority']})")

    else:
        st.error("No matching rule. Applicant not eligible for any scholarship.")
