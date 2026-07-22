# unity-headless-cli-skill

[![GitHub stars](https://img.shields.io/github/stars/Codeturion/unity-headless-cli-skill?style=flat)](https://github.com/Codeturion/unity-headless-cli-skill/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/Codeturion/unity-headless-cli-skill)](https://github.com/Codeturion/unity-headless-cli-skill/commits)
[![Issues](https://img.shields.io/github/issues/Codeturion/unity-headless-cli-skill)](https://github.com/Codeturion/unity-headless-cli-skill/issues)
[![License: MIT](https://img.shields.io/github/license/Codeturion/unity-headless-cli-skill)](LICENSE)
[![Unity](https://img.shields.io/badge/Unity-6000.x-000000?logo=unity)](https://unity.com)
[![status: experimental](https://img.shields.io/badge/status-experimental-orange)](#caveats)

A Claude Code plugin that sets up any Unity project to be driven **headless from the terminal**: no GUI editor, no MCP server. It adds the pipeline package, drops a reference doc into the project, and wires `CLAUDE.md` to point at it, so Claude (and you) can create GameObjects, add components, edit assets, run tests, and evaluate live C# over SSH, with 200 to 600 ms round trips and no recompile.

The heavy lifting is the Unity CLI plus its experimental `com.unity.pipeline` package. `unity command` and `unity command eval` *are* the tools; an agent with a terminal needs none of the MCP protocol.

## Install (Claude Code)

```text
/plugin marketplace add Codeturion/unity-headless-cli-skill
/plugin install unity-headless-cli@unity-headless-cli-skill
```

Then, from inside your Unity project, run the skill (ask Claude to "set up headless Unity" or invoke `unity-headless-cli`). It will:

1. Resolve the project root (asks first).
2. Ensure the Unity CLI is installed (asks before installing anything machine level).
3. Add `com.unity.pipeline` to the project (`unity pipeline install`).
4. Write `docs/unity-cli-ref.md` into the project.
5. Create or append `CLAUDE.md` with a **Headless Unity CLI** section pointing at that doc.
6. Print the one manual step left: launch a `-batchmode` editor and leave it running.

Every step is idempotent, so re-running the skill is safe. After this, future Claude sessions in the project pick up the workflow automatically via `CLAUDE.md`.

> The plugin ships the skill and a bundled reference. It does not install Unity, the CLI, or a running editor for you; it drives and configures them. The skill asks before any install.

## What is in here

```text
.claude-plugin/
  marketplace.json          # marketplace entry (add via /plugin marketplace add)
  plugin.json               # plugin manifest
skills/unity-headless-cli/
  SKILL.md                  # the bootstrap-and-drive skill
  reference/unity-cli-ref.md# reference copied into <project>/docs on setup
examples/MyPipelineCommands.cs  # custom [CliCommand] sample, compile ready
scripts/install.sh          # standalone CLI installer (no Claude needed)
```

## Use it without Claude

You do not need the plugin to use the workflow. Install the CLI and drive an editor directly:

```bash
./scripts/install.sh /path/to/your/project      # installs CLI, adds the package
Unity -batchmode -projectpath <project> -logFile editor.log   # NO -quit
unity command create_gameobject --name Spawner --components Light --project-path <project>
unity command eval "return Application.unityVersion;" --project-path <project>
```

Full command surface, custom commands, automation contract, and gotchas: [`skills/unity-headless-cli/reference/unity-cli-ref.md`](skills/unity-headless-cli/reference/unity-cli-ref.md).

## Why this beats a GUI bridge

An agent with a terminal needs none of the MCP protocol. `unity command` / `unity command eval` *are* the tools. Same capability as a stdio MCP bridge, but no GUI to keep open, no window to render, works headless over SSH, and drops straight into CI. The same terminal drives any project with `--project-path`.

## Caveats

- The CLI is beta and the package is experimental (`-exp`). Expect churn between versions.
- Stale Unity Hub keychain items can make every CLI command hang on an invisible GUI keychain prompt. Clear them if commands hang.
- `eval` runs arbitrary C# and is gated behind the pipeline server's localhost bearer token by design.

## Docs

- Unity CLI reference: https://docs.unity.com/en-us/unity-cli/unity-cli-reference
- Pipeline package: https://docs.unity3d.com/Packages/com.unity.pipeline@0.3

## License

MIT. See [LICENSE](LICENSE).
