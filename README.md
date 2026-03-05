# Getting Started with GitHub Copilot

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

Hey eloiza-souza!

Mona here. I'm done preparing your exercise. Hope you enjoy! 💚

Remember, it's self-paced so feel free to take a break! ☕️

[![](https://img.shields.io/badge/Go%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/eloiza-souza/skills-getting-started-with-github-copilot/issues/1)

## 🧪 Testing and CI

This repository includes a suite of backend tests under `tests/` that exercise `src/app.py` using FastAPI's test client. A GitHub Actions workflow (`.github/workflows/python-tests.yml`) automatically runs `pytest` on every push or pull request targeting `main`.

To run the tests locally:

```bash
pip install -r requirements.txt  # installs pytest + other deps
pytest -q
```

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

