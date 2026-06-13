"""Run local response-time and payload-size checks.

This does not emulate radio conditions packet-by-packet. It checks the parts the
project controls: server-side answer latency, SMS message length, and static UI
asset size. Those are the main determinants of 2G/3G usability before carrier
latency is added.
"""

from __future__ import annotations

import statistics
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.chatbot import WelfareChatbot  # noqa: E402

SCENARIOS = [
    ["1", "38 महिला", "गांव किसान जमीन", "राशन कच्चा घर गैस नहीं", "इलाज", "आधार बैंक राशन"],
    ["2", "28 ஆண்", "நகர டெலிவரி டிரைவர்", "குறைந்த வருமானம்", "இல்லை", "ஆதார் வங்கி"],
    ["3", "64 woman", "village labour", "ration kutcha house no LPG", "senior hospital", "aadhaar bank ration"],
    ["1", "24 महिला", "गांव मजदूर", "राशन", "गर्भवती बेटी", "आधार बैंक राशन"],
]


def run() -> int:
    bot = WelfareChatbot()
    durations_ms = []
    sms_lengths = []
    for index, scenario in enumerate(SCENARIOS, start=1):
        session = f"scenario-{index}"
        result = None
        for message in scenario:
            start = time.perf_counter()
            result = bot.chat(session, message, channel="sms")
            durations_ms.append((time.perf_counter() - start) * 1000)
        sms_lengths.append(len(result["reply"]) if result else 0)

    static_bytes = sum(path.stat().st_size for path in (ROOT / "static").glob("*") if path.is_file())
    print("JanSahayak quality check")
    print(f"median_engine_latency_ms={statistics.median(durations_ms):.2f}")
    print(f"p95_engine_latency_ms={statistics.quantiles(durations_ms, n=20)[18]:.2f}")
    print(f"max_sms_reply_chars={max(sms_lengths)}")
    print(f"static_asset_size_kb={static_bytes / 1024:.1f}")

    if statistics.median(durations_ms) > 3000:
        print("FAIL: median engine latency exceeds 3 seconds")
        return 1
    if max(sms_lengths) > 900:
        print("FAIL: SMS reply too long for low-bandwidth channel")
        return 1
    if static_bytes > 100 * 1024:
        print("FAIL: static UI exceeds 100 KB target")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
