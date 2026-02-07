# Skill: Godot Web Deploy Manager
## Description
Automates and troubleshoots GitHub Pages deployment for Godot 4.x games. Handles CI/CD workflows, Cross-Origin Isolation (COI) for SharedArrayBuffer, and common configuration errors.

## Usage
- **Deploy:** "Deploy this Godot project to GitHub"
- **Fix:** "Fix the Godot web build", "Game stuck on loading screen", "SharedArrayBuffer error"
- **Status:** "Check deployment status"

## Procedures

### 1. Diagnosis (Pre-flight Check)
When the user requests a deploy or reports an error, check these first:
1.  **Project Root:** Verify `project.godot` exists.
2.  **Main Scene:** Read `project.godot` and look for `run/main_scene`.
    - If missing: Ask user which `.tscn` is the main menu/gameplay and add it.
3.  **Export Presets:** Read `export_presets.cfg`.
    - Look for `[preset.X]` with `platform="Web"`.
    - If missing: Create a basic "Web" preset.

### 2. Symptom-Based Fixes

#### A. Symptom: "SharedArrayBuffer is not defined" / "Cross Origin Isolation"
*   **Cause:** Godot 4 Web export requires COI headers, which GitHub Pages doesn't send by default.
*   **Fix:** Inject `coi-serviceworker`.
*   **Action:** Update `.github/workflows/deploy.yml` to:
    1.  Download `coi-serviceworker.min.js` to the build output dir.
    2.  Use `sed` to inject `<script src="coi-serviceworker.min.js"></script>` into the `<head>` of `index.html`.
    *   *Note: Do this in the CI pipeline to keep source clean.*

#### B. Symptom: "No export template found" (CI Failure)
*   **Cause:** GitHub Actions runner lacks Godot templates.
*   **Fix:** Add template installation step to `deploy.yml`.
*   **Action:** Insert `wget` & `unzip` steps for `Godot_v4.x_export_templates.tpz` before the export command.

#### C. Symptom: Black Screen / "No main scene defined"
*   **Cause:** `project.godot` missing `run/main_scene`.
*   **Fix:** Set main scene.
*   **Action:** `edit project.godot` -> Add `run/main_scene="res://path/to/scene.tscn"`.

### 3. Workflow Template (deploy.yml)
Use the robust template below if creating a new workflow. It includes:
- Godot 4.2.1 Setup (Adjust version if user uses different one)
- Template Installation
- Web Export
- COI Fix (Service Worker)
- GitHub Pages Deploy

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: barichello/godot-ci:4.2.1
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Export Templates
        run: |
          mkdir -p ~/.local/share/godot/export_templates/4.2.1.stable
          wget -q https://github.com/godotengine/godot/releases/download/4.2.1-stable/Godot_v4.2.1-stable_export_templates.tpz
          unzip -q Godot_v4.2.1-stable_export_templates.tpz
          mv templates/* ~/.local/share/godot/export_templates/4.2.1.stable/
          rm Godot_v4.2.1-stable_export_templates.tpz
          rm -rf templates

      - name: Build & Export
        run: |
          mkdir -p build_output
          # Export to index.html
          godot --headless --verbose --export-release "Web" build_output/index.html
          
          # COI Fix
          wget -q https://github.com/gzuidhof/coi-serviceworker/raw/master/coi-serviceworker.min.js -O build_output/coi-serviceworker.min.js
          sed -i 's|<head>|<head><script src="coi-serviceworker.min.js"></script>|g' build_output/index.html
          
          # NoJekyll for _ underscore folders
          touch build_output/.nojekyll

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build_output

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```
