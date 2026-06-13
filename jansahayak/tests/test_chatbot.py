import unittest

from src.chatbot import WelfareChatbot


class ChatbotFlowTests(unittest.TestCase):
    def run_flow(self, answers):
        bot = WelfareChatbot()
        session = "test"
        result = None
        for answer in answers:
            result = bot.chat(session, answer)
        self.assertIsNotNone(result)
        return result, bot.sessions[session]

    def test_farmer_gets_pm_kisan_and_pmayg(self):
        result, session = self.run_flow(
            [
                "1",
                "38 महिला",
                "गांव किसान जमीन",
                "राशन कच्चा घर गैस नहीं",
                "इलाज",
                "आधार बैंक राशन",
            ]
        )
        ids = [item["scheme"]["id"] for item in session.recommendations]
        self.assertIn("pm_kisan", ids)
        self.assertIn("pmay_g", ids)
        self.assertIn("pmuy", ids)
        self.assertEqual(result["state"], "recommendations")

    def test_tamil_gig_worker_gets_eshram_and_apy(self):
        _result, session = self.run_flow(
            [
                "2",
                "28 ஆண்",
                "நகர டெலிவரி டிரைவர்",
                "குறைந்த வருமானம்",
                "இல்லை",
                "ஆதார் வங்கி",
            ]
        )
        ids = [item["scheme"]["id"] for item in session.recommendations]
        self.assertIn("eshram", ids)
        self.assertIn("apy", ids)

    def test_code_mixed_aadhaar_lost_response_is_grounded(self):
        bot = WelfareChatbot()
        session = "aadhaar"
        for answer in ["1", "31 महिला", "गांव मजदूर", "राशन", "नहीं", "aadhaar खो गया bank ration"]:
            result = bot.chat(session, answer)
        self.assertIn("आधार", result["reply"])
        self.assertIn("CSC", result["reply"])

    def test_checklist_selection_after_recommendation(self):
        bot = WelfareChatbot()
        session = "checklist"
        for answer in ["3", "34 woman", "village labour", "ration no LPG", "pregnant girl below 10", "aadhaar bank ration"]:
            bot.chat(session, answer)
        result = bot.chat(session, "1")
        self.assertEqual(result["state"], "checklist")
        self.assertIn("Document checklist", result["reply"])

    def test_unknown_answer_refuses_to_hallucinate(self):
        bot = WelfareChatbot()
        session = "unknown"
        for answer in ["3", "34 woman", "city other", "none", "none", "bank"]:
            bot.chat(session, answer)
        result = bot.chat(session, "Can I get a scheme for buying a tractor drone?")
        self.assertIn("do not have enough grounded information", result["reply"])


if __name__ == "__main__":
    unittest.main()
