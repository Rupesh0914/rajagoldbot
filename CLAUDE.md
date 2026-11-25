# CLAUDE.md

Guidance for any assistant working in this repo.

- The owner is learning the strategy while the bot is built. Every new bot piece ships with a
  lesson in `lessons/` written in plain English, a "check yourself" quiz, and tests. Follow the
  roadmap in `README.md` in order; do not build ahead of the lessons.
- Explain in plain English. No jargon without a one-line definition.
- Demo account only. Never switch anything to a real-money account or enter a real account
  number: that is the owner's action, by hand, in MetaTrader.
- Never commit, print or log passwords, API keys or account numbers.
- The bot acts on closed candles only and never looks ahead. Every piece needs a test that its
  past output does not change when later data arrives.
- No strategy setting is tuned on test results. The honest-testing rules arrive in lesson 9 and
  are fixed before data is seen.
- Standard-library Python (plus `tzdata`). Tests: `python -m unittest discover -s tests -t .`
