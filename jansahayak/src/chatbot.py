"""Grounded multilingual welfare scheme chatbot engine.

The engine is intentionally deterministic: it never invents scheme facts. It
selects from a local catalogue, cites the scheme source URL, and tells the user
when final verification is needed.
"""

from __future__ import annotations

import json
import re
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .i18n import LANGUAGE_NAMES, SUPPORTED_LANGUAGES, t


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "schemes.json"

YES_TOKENS = {
    "yes",
    "y",
    "haan",
    "ha",
    "hai",
    "h",
    "हाँ",
    "हा",
    "हां",
    "ஆம்",
    "aama",
    "ama",
    "உள்ளது",
}
NO_TOKENS = {
    "no",
    "n",
    "nahi",
    "nahin",
    "none",
    "नहीं",
    "नही",
    "இல்லை",
    "illa",
    "illai",
}

QUESTION_ORDER = [
    "age_gender",
    "location_work",
    "income_assets",
    "family_needs",
    "docs",
]


def load_catalogue(path: Path = DATA_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    return text.strip().lower()


def compact(text: str, limit: int = 1450) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def detect_language(text: str) -> str | None:
    lowered = normalize_text(text)
    if lowered in {"1", "hi", "hindi", "हिंदी", "हिन्दी"}:
        return "hi"
    if lowered in {"2", "ta", "tamil", "தமிழ்", "tamizh"}:
        return "ta"
    if lowered in {"3", "en", "eng", "english"}:
        return "en"
    if re.search(r"[\u0B80-\u0BFF]", text):
        return "ta"
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"
    return None


def contains_any(text: str, tokens: list[str] | set[str]) -> bool:
    lowered = normalize_text(text)
    return any(token in lowered for token in tokens)


def parse_age(text: str) -> int | None:
    match = re.search(r"\b(1[89]|[2-9][0-9]|10[0-9])\b", text)
    return int(match.group(1)) if match else None


def parse_answer(profile: dict[str, Any], question: str, text: str) -> None:
    lowered = normalize_text(text)
    tokens = set(re.findall(r"[\w\u0900-\u097F\u0B80-\u0BFF]+", lowered))

    if question == "age_gender":
        age = parse_age(lowered)
        if age:
            profile["age"] = age
        if contains_any(lowered, ["woman", "female", "mahila", "ladki", "महिला", "औरत", "लड़की", "பெண்"]):
            profile["gender"] = "female"
        elif contains_any(lowered, ["man", "male", "purush", "पुरुष", "आदमी", "ஆண்"]):
            profile["gender"] = "male"

    elif question == "location_work":
        if contains_any(lowered, ["village", "rural", "gaon", "gram", "गांव", "ग्राम", "ग्रामीण", "கிராம"]):
            profile["rural"] = True
        if contains_any(lowered, ["city", "urban", "town", "शहर", "नगर", "நகர"]):
            profile["rural"] = False
        if contains_any(lowered, ["farmer", "kisan", "खेती", "किसान", "விவசாய", "farmland", "land"]):
            profile["occupation"] = "farmer_land"
        elif contains_any(lowered, ["labour", "labor", "mazdoor", "मजदूर", "कामगार", "கூலி", "தொழிலாளர்"]):
            profile["occupation"] = "labour"
        elif contains_any(lowered, ["delivery", "gig", "driver", "auto", "platform", "domestic", "maid", "ठेला", "रेहड़ी", "ड्राइवर", "டெலிவரி", "டிரைவர்"]):
            profile["occupation"] = "gig_unorganised"
        elif contains_any(lowered, ["unemployed", "काम नहीं", "வேலை இல்லை"]):
            profile["occupation"] = "unemployed"

    elif question == "income_assets":
        if contains_any(lowered, ["bpl", "ration", "antyodaya", "poor", "low income", "कम आय", "गरीब", "राशन", "ஏழை", "ரேஷன்", "குறைந்த வருமான"]):
            profile["low_income"] = True
            profile["ration_card"] = True
        if contains_any(lowered, ["kutcha", "kaccha", "कच्चा", "झोपड़ी", "homeless", "no house", "வீடு இல்லை", "குடிசை"]):
            profile["housing"] = "kutcha"
        if contains_any(lowered, ["no lpg", "no gas", "gas nahi", "gas nahin", "गैस नहीं", "lpg नहीं", "எரிவாயு இல்லை", "lpg இல்லை"]):
            profile["no_lpg"] = True
        if tokens & NO_TOKENS and "low_income" not in profile and "housing" not in profile and "no_lpg" not in profile:
            profile["low_income"] = False

    elif question == "family_needs":
        if contains_any(lowered, ["pregnant", "pregnancy", "lactating", "mother", "गर्भ", "गर्भवती", "स्तनपान", "கர்ப்ப", "பாலூட்ட"]):
            profile["pregnant_lactating"] = True
        if contains_any(lowered, ["girl", "daughter", "beti", "below 10", "under 10", "बेटी", "लड़की", "10 साल", "பெண் குழந்தை", "மகள்"]):
            profile["girl_child_under10"] = True
        if contains_any(lowered, ["senior", "old", "elder", "60", "70", "बुजुर्ग", "वृद्ध", "முதியோர்", "மூத்த"]):
            profile["senior_or_elder"] = True
        if contains_any(lowered, ["widow", "विधवा", "கைம்பெண்", "விதவை"]):
            profile["widow"] = True
        if contains_any(lowered, ["disabled", "disability", "दिव्यांग", "विकलांग", "மாற்றுத்திறன்"]):
            profile["disabled"] = True
        if contains_any(lowered, ["hospital", "health", "इलाज", "अस्पताल", "மருத்துவ", "சிகிச்சை"]):
            profile["health_need"] = True
        if tokens & NO_TOKENS and not any(
            profile.get(k)
            for k in ["pregnant_lactating", "girl_child_under10", "senior_or_elder", "widow", "disabled", "health_need"]
        ):
            profile["no_special_need"] = True

    elif question == "docs":
        lost = contains_any(lowered, ["lost", "missing", "kho", "खो", "गुम", "தொலை", "காணவில்லை"])
        if contains_any(lowered, ["aadhaar", "adhar", "aadhar", "आधार", "ஆதார்"]):
            profile["aadhaar"] = not lost
            if lost:
                profile["aadhaar_lost"] = True
        if contains_any(lowered, ["bank", "passbook", "account", "बैंक", "खाता", "வங்கி", "கணக்கு"]):
            profile["bank"] = not (lost and not contains_any(lowered, ["aadhaar", "आधार", "ஆதார்"]))
        if contains_any(lowered, ["ration", "राशन", "ரேஷன்"]):
            profile["ration_card"] = not (lost and not contains_any(lowered, ["aadhaar", "आधार", "ஆதார்"]))


def is_unorganised(profile: dict[str, Any]) -> bool:
    return profile.get("occupation") in {"labour", "gig_unorganised", "unemployed"}


def scheme_score(scheme_id: str, profile: dict[str, Any]) -> tuple[int, list[str], list[str]]:
    score = 0
    reasons: list[str] = []
    missing: list[str] = []
    age = profile.get("age")
    rural = profile.get("rural")
    low_income = profile.get("low_income")

    def add(points: int, reason: str) -> None:
        nonlocal score
        score += points
        reasons.append(reason)

    if scheme_id == "pm_kisan":
        if profile.get("occupation") == "farmer_land":
            add(5, "farmer_land")
        else:
            missing.append("cultivable land record")
        if rural is True:
            add(2, "rural_household")
        if age and age >= 18:
            add(1, "adult")

    elif scheme_id == "pmjay":
        if low_income or profile.get("ration_card"):
            add(4, "low_income_or_ration")
        if profile.get("senior_or_elder") or (age and age >= 70):
            add(3, "senior_citizen")
        if profile.get("health_need"):
            add(2, "health_need")
        if score == 0:
            missing.append("official beneficiary list match")

    elif scheme_id == "pmay_g":
        if rural is True:
            add(2, "rural_household")
        else:
            missing.append("rural residence")
        if profile.get("housing") == "kutcha":
            add(5, "kutcha_or_no_house")
        else:
            missing.append("kutcha/no-house condition")

    elif scheme_id == "pmuy":
        if profile.get("no_lpg"):
            add(4, "no_lpg_connection")
        else:
            missing.append("no existing LPG connection")
        if low_income or profile.get("ration_card"):
            add(3, "poor_household")
        else:
            missing.append("poor household/deprivation proof")
        if profile.get("gender") == "female":
            add(1, "adult_woman_applicant")
        else:
            missing.append("adult woman applicant")

    elif scheme_id == "mgnrega":
        if rural is True:
            add(3, "rural_household")
        else:
            missing.append("rural residence")
        if age and age >= 18:
            add(2, "adult_worker")
        if profile.get("occupation") in {"labour", "unemployed", "farmer_land"}:
            add(3, "manual_work_likelihood")

    elif scheme_id == "ssy":
        if profile.get("girl_child_under10"):
            add(6, "girl_child_under10")
        else:
            missing.append("girl child below 10")

    elif scheme_id == "pmmvy":
        if profile.get("pregnant_lactating"):
            add(6, "pregnant_or_lactating")
        else:
            missing.append("pregnancy/lactation status")
        if profile.get("gender") == "female":
            add(1, "woman_beneficiary")

    elif scheme_id == "eshram":
        if is_unorganised(profile):
            add(6, "unorganised_or_gig_worker")
        else:
            missing.append("unorganised work status")
        if age and 16 <= age <= 59:
            add(1, "working_age")

    elif scheme_id == "apy":
        if age and 18 <= age <= 40:
            add(4, "age_18_40")
        else:
            missing.append("age 18-40")
        if is_unorganised(profile):
            add(2, "unorganised_worker")
        if profile.get("bank"):
            add(1, "bank_account")
        else:
            missing.append("bank account")

    elif scheme_id == "nsap":
        if low_income or profile.get("ration_card"):
            add(3, "low_income_or_bpl")
        else:
            missing.append("BPL/low-income proof")
        if profile.get("senior_or_elder") or (age and age >= 60):
            add(4, "elderly")
        if profile.get("widow"):
            add(4, "widow")
        if profile.get("disabled"):
            add(4, "disability")
        if score <= 3:
            missing.append("age/widow/disability category")

    return score, reasons, missing


def confidence_label(score: int, missing: list[str]) -> str:
    if score >= 7 and len(missing) <= 1:
        return "likely"
    if score >= 5:
        return "needs_verification"
    return "low"


def localised(item: dict[str, Any], key: str, lang: str) -> Any:
    value = item.get(key, {})
    if isinstance(value, dict):
        return value.get(lang) or value.get("en")
    return value


def render_recommendations(recommendations: list[dict[str, Any]], lang: str, sms: bool = False) -> str:
    if not recommendations:
        return t("no_recommendations", lang)
    lines = [t("recommendations_intro", lang)]
    for index, rec in enumerate(recommendations, start=1):
        scheme = rec["scheme"]
        name = localised(scheme, "name", lang)
        benefit = localised(scheme, "benefit", lang)
        source = scheme["source"]["url"]
        confidence = rec["confidence"].replace("_", " ")
        if sms:
            lines.append(f"{index}. {name}: {scheme['sms_hint'][lang]} ({confidence})")
        else:
            lines.append(f"{index}. {name} [{confidence}]\n   {benefit}\n   {t('source_title', lang)}: {source}")
    lines.append(t("checklist_prompt", lang))
    return compact("\n".join(lines), 850 if sms else 2200)


def render_checklist(scheme: dict[str, Any], lang: str, sms: bool = False) -> str:
    name = localised(scheme, "name", lang)
    docs = localised(scheme, "documents", lang)
    steps = localised(scheme, "apply_steps", lang)
    if sms:
        doc_text = "; ".join(docs)
        return compact(f"{name} - {t('checklist_title', lang)}: {doc_text}. {scheme['sms_hint'][lang]}", 700)
    lines = [
        f"{name}",
        f"{t('checklist_title', lang)}:",
        *[f"- {doc}" for doc in docs],
        f"{t('steps_title', lang)}:",
        *[f"{i}. {step}" for i, step in enumerate(steps, start=1)],
        f"{t('source_title', lang)}: {scheme['source']['url']}",
    ]
    return "\n".join(lines)


@dataclass
class ChatSession:
    session_id: str
    lang: str | None = None
    question_index: int = 0
    profile: dict[str, Any] = field(default_factory=dict)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    completed: bool = False
    updated_at: float = field(default_factory=time.time)

    @property
    def current_question(self) -> str | None:
        if self.question_index >= len(QUESTION_ORDER):
            return None
        return QUESTION_ORDER[self.question_index]


class WelfareChatbot:
    def __init__(self, catalogue: dict[str, Any] | None = None):
        self.catalogue = catalogue or load_catalogue()
        self.schemes = self.catalogue["schemes"]
        self.sessions: dict[str, ChatSession] = {}

    def get_session(self, session_id: str) -> ChatSession:
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatSession(session_id=session_id)
        return self.sessions[session_id]

    def reset_session(self, session_id: str) -> ChatSession:
        self.sessions[session_id] = ChatSession(session_id=session_id)
        return self.sessions[session_id]

    def recommend(self, profile: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
        ranked: list[dict[str, Any]] = []
        for scheme in self.schemes:
            score, reasons, missing = scheme_score(scheme["id"], profile)
            if score >= 4:
                ranked.append(
                    {
                        "scheme": scheme,
                        "score": score,
                        "reasons": reasons,
                        "missing": missing,
                        "confidence": confidence_label(score, missing),
                    }
                )
        ranked.sort(key=lambda rec: rec["score"], reverse=True)
        return ranked[:limit]

    def find_scheme(self, text: str, recommendations: list[dict[str, Any]] | None = None) -> dict[str, Any] | None:
        lowered = normalize_text(text)
        if lowered.isdigit() and recommendations:
            index = int(lowered) - 1
            if 0 <= index < len(recommendations):
                return recommendations[index]["scheme"]
        for scheme in self.schemes:
            if scheme["id"] in lowered:
                return scheme
            names = scheme["name"].values()
            if any(normalize_text(name) in lowered for name in names):
                return scheme
            if any(token in lowered for token in scheme.get("tags", [])):
                return scheme
        return None

    def retrieve_answer(self, text: str, lang: str, session: ChatSession, sms: bool = False) -> str:
        lowered = normalize_text(text)
        if contains_any(lowered, ["aadhaar", "adhar", "aadhar", "आधार", "ஆதார்"]) and contains_any(
            lowered, ["lost", "missing", "kho", "खो", "गुम", "தொலை", "காணவில்லை"]
        ):
            return t("aadhaar_lost", lang)

        scheme = self.find_scheme(text, session.recommendations)
        if scheme:
            if contains_any(lowered, ["doc", "document", "kagaz", "paper", "checklist", "कागज", "दस्तावेज", "ஆவணம்"]):
                return render_checklist(scheme, lang, sms=sms)
            summary = localised(scheme, "plain_summary", lang)
            benefit = localised(scheme, "benefit", lang)
            source = scheme["source"]["url"]
            return compact(f"{localised(scheme, 'name', lang)}\n{summary}\n{benefit}\n{t('source_title', lang)}: {source}", 700 if sms else 1400)

        if contains_any(lowered, ["honest", "hallucinat", "source", "पक्का", "झूठ", "ஆதாரம்"]):
            return t("honesty_note", lang)

        return t("unknown", lang)

    def chat(self, session_id: str, text: str, channel: str = "web") -> dict[str, Any]:
        sms = channel in {"sms", "whatsapp", "ivr"}
        normalized = normalize_text(text)
        session = self.get_session(session_id)
        session.updated_at = time.time()

        if normalized in {"restart", "reset", "start over", "फिर शुरू", "रीस्टार्ट", "மீண்டும்"}:
            session = self.reset_session(session_id)
            return {
                "session_id": session_id,
                "reply": f"{t('restart', 'en')}\n{t('choose_language', 'en')}",
                "profile": session.profile,
                "recommendations": [],
                "state": "language",
            }

        if not session.lang:
            detected = detect_language(text)
            if not detected:
                return {
                    "session_id": session_id,
                    "reply": t("choose_language", "en"),
                    "profile": session.profile,
                    "recommendations": [],
                    "state": "language",
                }
            session.lang = detected if detected in SUPPORTED_LANGUAGES else "en"
            lang = session.lang
            return {
                "session_id": session_id,
                "reply": f"{t('welcome', lang)}\n{t('q_age_gender', lang)}",
                "profile": session.profile,
                "recommendations": [],
                "state": "question",
            }

        lang = session.lang

        if session.completed:
            scheme = self.find_scheme(text, session.recommendations)
            if scheme and (normalized.isdigit() or contains_any(normalized, ["doc", "document", "कागज", "ஆவணம்", "checklist"])):
                return {
                    "session_id": session_id,
                    "reply": render_checklist(scheme, lang, sms=sms),
                    "profile": session.profile,
                    "recommendations": self._public_recommendations(session, lang),
                    "state": "checklist",
                }
            return {
                "session_id": session_id,
                "reply": self.retrieve_answer(text, lang, session, sms=sms),
                "profile": session.profile,
                "recommendations": self._public_recommendations(session, lang),
                "state": "answer",
            }

        question = session.current_question
        if question:
            parse_answer(session.profile, question, text)
            session.question_index += 1

        if session.question_index < len(QUESTION_ORDER):
            next_question = QUESTION_ORDER[session.question_index]
            return {
                "session_id": session_id,
                "reply": t(f"q_{next_question}", lang),
                "profile": session.profile,
                "recommendations": [],
                "state": "question",
            }

        session.completed = True
        session.recommendations = self.recommend(session.profile)
        reply_parts = []
        if session.profile.get("aadhaar_lost"):
            reply_parts.append(t("aadhaar_lost", lang))
        reply_parts.append(render_recommendations(session.recommendations, lang, sms=sms))
        return {
            "session_id": session_id,
            "reply": "\n".join(reply_parts),
            "profile": session.profile,
            "recommendations": self._public_recommendations(session, lang),
            "state": "recommendations",
        }

    def _public_recommendations(self, session: ChatSession, lang: str) -> list[dict[str, Any]]:
        output = []
        for rec in session.recommendations:
            scheme = rec["scheme"]
            output.append(
                {
                    "id": scheme["id"],
                    "name": localised(scheme, "name", lang),
                    "benefit": localised(scheme, "benefit", lang),
                    "source": scheme["source"],
                    "confidence": rec["confidence"],
                    "missing": rec["missing"],
                    "score": rec["score"],
                }
            )
        return output


def demo_conversation() -> list[str]:
    bot = WelfareChatbot()
    session = "demo"
    messages = ["1", "38 महिला", "गांव किसान जमीन", "राशन कच्चा घर गैस नहीं", "10 साल से कम बेटी इलाज", "आधार बैंक राशन"]
    return [bot.chat(session, msg)["reply"] for msg in messages]
