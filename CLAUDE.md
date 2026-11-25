# CLAUDE.md

Guidance for any assistant working in this repo.

- The owner is learning the strategy while the bot is built. Every new bot piece ships with a
  lesson in `lessons/` written in plain English, a "check yourself" quiz, and tests. Follow the
  roadmap in `README.md` in order; do not build ahead of the lessons.
- `COVERAGE.md` maps every rule and setup in the owner's research notes to a lesson, and lists
  every number the bot had to choose. Update it with each lesson. A number the notes do not give
  is recorded there as our choice, never presented as a Raja Banks rule.
- Explain in plain English. No jargon without a one-line definition.
- Demo account only. Never switch anything to a real-money account or enter a real account
  number: that is the owner's action, by hand, in MetaTrader.
- Never commit, print or log passwords, API keys or account numbers.
- The bot acts on closed candles only and never looks ahead. Every piece needs a test that its
  past output does not change when later data arrives.
- Price history is split in `research/DATA_SPLIT.md`. Ideas may be tried, fixed and tried again
  on the development part only. Never load, print or summarise a bar from the validation or
  holdout parts by any means other than `research/final_test.py`, which opens each once under
  the frozen rules in `research/PROTOCOL.md`. Never edit `PROTOCOL.md` or the candidates in
  `final_test.py`. A development result is a clue, never called proof.
- Standard-library Python (plus `tzdata`). Tests: `python -m unittest discover -s tests -t .`
