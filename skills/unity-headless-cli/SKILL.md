---
name: unity-headless-cli
description: Set up the current Unity project to be driven headless from the terminal (no GUI, no MCP server), then use that workflow. On invocation it adds com.unity.pipeline, writes docs/unity-cli-ref.md, and points CLAUDE.md at it, so this and future Claude sessions can create GameObjects, add components, edit assets, run tests, and evaluate live C# over SSH. Use when the user wants to "set up headless Unity", "drive Unity from the terminal", "add the unity CLI to this project", or run Unity in CI.
license: MIT
---

# Unity Headless CLI: setup and use

This skill has two jobs. First, **bootstrap** the current project so it can be driven headless. Second, **drive** it with `unity command` / `unity command eval`. Round trips are 200 to 600 ms with no recompile and no domain reload.

If the project already looks set up (CLAUDE.md points at `docs/unity-cli-ref.md` and the package is present), skip the bootstrap and go straight to "Drive it".

## Bootstrap (run once per project)

Do these in order. Confirm before anything that installs software or edits files. Each step is idempotent, so re-running the skill is safe.

### 1. Resolve the project root

Use the current git repo root (`git rev-parse --show-toplevel`), or the directory the user names. Confirm the path with the user before continuing. Call it `<root>`.

### 2. Ensure the Unity CLI is installed

```bash
unity --version
```

If that fails, tell the user you need to install the Unity CLI (beta) and ask to proceed. On yes:

```bash
curl -fsSL https://public-cdn.cloud.unity3d.com/hub/prod/cli/install.sh | UNITY_CLI_CHANNEL=beta bash
```

The CLI is machine level, so never install it silently. If the user declines, stop and report what is missing.

### 3. Add the pipeline package to the project

```bash
unity pipeline install --project-path <root>
```

This adds `com.unity.pipeline` to `Packages/manifest.json`. If it is already present, this is a no-op.

### 4. Write the reference doc

Copy the bundled reference into the project so it lives with the code:

```bash
mkdir -p <root>/docs
cp "${CLAUDE_PLUGIN_ROOT}/skills/unity-headless-cli/reference/unity-cli-ref.md" <root>/docs/unity-cli-ref.md
```

(`${CLAUDE_PLUGIN_ROOT}` is the installed plugin's directory. If it is not set, use this skill's own folder as the source.) If `docs/unity-cli-ref.md` already exists, overwrite it only after confirming, so you do not clobber local edits.

### 5. Wire up CLAUDE.md

Point the project's instructions at the reference so every future session knows about it, mirroring how a project links its own docs.

- If `<root>/CLAUDE.md` does not exist, create it with the section below.
- If it exists and does not already contain a "Headless Unity CLI" section, append the section below.
- If the section is already there, leave it alone.

Section to add:

```markdown
## Headless Unity CLI

This project can be driven headless from the terminal (no GUI, no MCP server) via the
Unity CLI + `com.unity.pipeline`. Commands: `unity command <tool> --project-path <p>`
and `unity command eval "<C#>" --project-path <p>`. Full reference, install, custom
commands, and gotchas: [docs/unity-cli-ref.md](docs/unity-cli-ref.md).
```

### 6. Report and hand off

Print a short summary of what changed (package added, `docs/unity-cli-ref.md` written, CLAUDE.md updated) and the one manual step that remains: launch a headless editor and leave it running.

```bash
# NO -quit; leave it running, then commands can reach it
Unity -batchmode -projectpath <root> -logFile editor.log
```

On a display less machine never launch the GUI editor: it hangs in AppKit startup. Always `-batchmode`.

## Drive it

Once a headless editor is running for the project:

```bash
# discover the tools this editor exposes
unity command --project-path <root>

# built in commands
unity command create_gameobject --name Spawner --components Light --project-path <root>
unity command add_component --gameobject Spawner --component Rigidbody --project-path <root>
unity command find_assets --query "t:Prefab" --project-path <root>

# live C# on the editor main thread
unity command eval "return Application.unityVersion;" --project-path <root>
unity command eval_file snippet.cs --project-path <root>

# tests and builds
unity command run_tests --project-path <root>
```

Prefer `--project-path`. `unity pipeline list` may report a batchmode editor as "not reachable" even while commands work; trust `unity command`, not the list.

### Custom commands

Any static method tagged `[CliCommand]` in an Editor assembly becomes a tool automatically, no registration. Use `MainThreadRequired` for anything touching engine state; `RuntimeOnly` for dev-Player-only commands.

### Many projects

The same terminal drives any project. Loop:

```bash
for P in game-alpha puzzle-proto runner-3d; do
  unity command create_gameobject --name Spawner --project-path "$P"
done
```

## Gotchas

- The CLI is beta and the package is experimental (`-exp`). Expect churn between versions.
- Stale Unity Hub keychain items can make every CLI command hang on an invisible GUI keychain prompt (`--non-interactive` hangs too). Clear the stale keychain items.
- `eval` runs arbitrary C# and is gated behind the pipeline server's localhost bearer token by design. Treat it with the same care as running project code.

Full detail lives in `docs/unity-cli-ref.md` after bootstrap, or in `reference/unity-cli-ref.md` in this skill.
