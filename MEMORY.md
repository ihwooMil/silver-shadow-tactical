# MEMORY.md - Long-Term Memory

## Project Context
- **Game Development:**
  - '슬더스류'(Slay the Spire style) 게임 개발 중. [2026-02-05]
  - **New Project: "Project Wall & Abyss" [디펜스오펜스게임]**
    - Godot Engine 4.x 기반. 디펜스 + 던전 탐험 하이브리드.
    - GitHub(ihwooMil/project-wall-and-abyss) 연동 및 자동 배포(CI/CD) 구축 시도 중. [2026-02-06]
    - **🔥 CRITICAL STATUS (2026-02-06 17:35):**
        - **Issue:** Web deployment failing (404 / logs missing).
        - **Current Attempt:** "Version Blue 4" pushed.
        - **Fix Applied:** Changed GitHub Actions to append logs directly to `index.html` line-by-line (avoiding file creation issues).
        - **Next Action:** Check [Deployment Link](https://ihwooMil.github.io/project-wall-and-abyss/) for "VERSION: BLUE 4" and error logs.
