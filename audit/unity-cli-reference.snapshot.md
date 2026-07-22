# Snapshot of https://docs.unity.com/en-us/unity-cli/unity-cli-reference
# Normalized text only; regenerate with audit/snapshot.py

Unity command-line interface (CLI) reference • Unity command-line interface (CLI) • Unity Docs
Unity command-line interface (CLI) reference
Explore the Unity CLI commands, options, output formats, and exit codes you can use to install and manage Unity Editors and modules from a terminal.
Note
The Unity CLI is experimental.
Find the commands and options available in the Unity CLI. For installation and common task instructions, refer to Use the Unity CLI .
To use the Unity CLI to control the Unity Editor install and setup the Unity pipeline package .
Run unity --help
to check the authoritative command list for your installed version, including any commands not yet covered on this page.
Commands
Command
Alias
Description
install
i
Install a Unity Editor version, optionally with modules.
install-modules
im
Add modules to an already-installed Editor.
uninstall
u
Remove an installed Editor.
editors
e
List available releases and installed Editors, add local installs, and set the default Editor.
install-path
ip
Show or change the path where the CLI installs Editors.
open
Open a Unity project, resolving the correct Editor version.
projects
p
Manage the list of Unity projects the Hub knows about.
auth
a
Sign in, check login state, or sign out.
language
lang
Show or change the CLI display language.
upgrade
Self-update the unity
CLI binary.
help
Display help for any command. Equivalent to --help
.
Help commands
Command
Description
unity --help
Top-level help, including the list of commands.
unity <command> --help
Help for a specific command and its options.
unity <command> <subcommand> --help
Help for a subcommand (for example, unity editors add --help
).
Tip
unity --help
is the authoritative source for flags in your installed version. This page covers the main commands. Your release might add flags or commands that appear only in --help
.
Update the CLI
Use the built-in self-update command to install the latest CLI release:
unity upgrade
Install an Editor
Install a Unity Editor version, optionally with modules.
unity install [version] [options]
The version
argument is positional and optional:
On an interactive terminal, omitting the version opens an interactive prompt.
On a non-interactive terminal (for example, a CI pipeline), omitting the version is an error.
Version aliases
Alias
Resolves to
latest
The newest available Editor release.
lts
The newest long-term support release.
default
The version configured as your default in the Unity CLI.
6
, 6.5
, 2022
, and similar The newest release within that major or minor stream.
Install options
Refer to unity install --help
for the complete list.
Option
Usage
Description
-c, --changeset <hash>
-c 9b001d489a54
Changeset for the chosen Editor, required when the version isn't in the release list.
-m, --module <id>
-m android
or -m ios webgl
Module IDs to install alongside the Editor. Accepts multiple values.
--cm
, --childModules
--cm
Also install child modules of each selected module (for example, Android SDK & NDK under android
).
-a, --architecture <arch>
-a arm64
or -a x86_64
macOS only. Selects between Apple silicon and Intel builds.
Install examples
unity install 6000.3.7f1 unity install lts unity install 6000.3.7f1 -c 9b001d489a54 unity install 6000.3.7f1 -m android --cm unity install lts -m ios android webgl
Note
For available module IDs, refer to Add modules to a Unity Editor installation and the module ID table .
Install modules for an existing Editor
Add one or more modules to an Editor you already installed with the Hub or the CLI.
unity install-modules [options]
Important
You can only add modules to Editors that the Hub or CLI installed. Reinstall manually installed Editors through the Hub or CLI to add modules.
Install-modules options
Option
Required?
Description
-e, --editor-version <version>
No Editor version to add the module to. If omitted on an interactive terminal, you receive a prompt.
-m, --module <id>
No Module ID(s) to install. Accepts multiple values.
-l, --list
No List installable modules for the target Editor instead of installing anything.
--all
No Install every available module for the target Editor.
--cm
, --childModules
No Also install child modules. Use --no-cm
(or --no-childModules
) to explicitly skip them.
Install-modules examples
unity install-modules -e 6000.3.7f1 -m ios android unity install-modules -e 6000.3.7f1 -l unity install-modules -e 6000.3.7f1 --all unity install-modules -e 6000.3.7f1 -m android --no-cm
Uninstall an Editor
Remove an installed Editor version.
unity uninstall <version>
uninstall examples
unity uninstall 6000.3.7f1
List and manage Editors
Inspect available releases and installed Editors, register locally installed Editors with the Hub, and set a default version.
unity editors [options] unity editors add <path...> unity editors default [version]
Editor options
Option
Alias
Description
--releases
-r
Show available releases.
--installed
-i
Show Editors installed on this machine.
--verbose
Include additional detail in the output.
--architecture <architecture>
-a
Set Editor architecture (x86_64 or arm64) the default setting is "unknown".
--json
N/A Output the list in JSON format.
--watch
-w
Watch for editor changes and refresh output (press Ctrl-C to stop).
--help
-h
Display help for this command.
Add an Editor
Register an Editor you installed outside the Hub so the Hub and CLI can manage it. Accepts one or more paths.
unity editors add /Applications/Unity/Hub/Editor/6000.3.7f1/Unity.app unity editors add "C:\Program Files\Unity\6000.3.7f1" "C:\Program Files\Unity\2022.3.40f1"
Identify the default Editor
Print the current default Editor, or set a new default by passing a version:
unity editors default # show the default unity editors default 6000.3.7f1 # set the default
Editor command examples
unity editors -r # list available releases unity editors -i # list installed Editors unity editors -a # combined list
Set or get the Editor install path
Show or change the directory where the CLI installs Unity Editors.
unity install-path [options]
Alias: ip
. Run unity install-path --help
for the current option list, including flags to display or update the path.
Open a project
Open a Unity project, resolving the Editor version declared by the project.
unity open <path>
You can omit the open
keyword when the first argument is a path:
unity open ./MyProject unity ./MyProject # equivalent
Manage projects in the Hub registry
Manage the list of Unity projects the Hub knows about, so both the Hub UI and the CLI can find and open them.
unity projects [subcommand] [options]
Alias: p
. Run unity projects --help
to check the available commands and options in your installed CLI version.
Sign in and out
The auth
command manages your Unity account session.
unity auth login unity auth status unity auth logout
Command
Description
unity auth login
Opens a browser-based sign-in flow.
unity auth status
Prints the current signed-in user, if any.
unity auth logout
Signs out of the current session.
Change the CLI display language
Show the current CLI display language, or change it to a supported language.
unity language [options]
Alias: lang
. Run unity language --help
for the list of supported languages and the exact option names.
Output formats and automation
The CLI chooses a default output format based on the context and supports explicit formats for automation.
Format selection
Format
Selected when
Notes
human
Output goes to an interactive terminal. Colorized, animated progress, aligned columns.
tsv
Output goes to a pipe or file. Tab-separated, one record per line. Machine-parseable.
json
You set --format json
(or --json
). Structured output for use with jq
and other tools.
Select a format explicitly with the global flag:
unity editors -i --format json unity editors -i --format tsv
Tip
When you pipe CLI output, the default format changes to tab-separated values (TSV). If a script expects human-readable text, set --format human
explicitly, or parse TSV or JSON instead.
Error output
The CLI writes errors and diagnostic messages to stderr
, leaving stdout
free for data output. In JSON mode, the CLI emits errors as {"error": "..."}
on stderr
.
To capture both streams in a shell:
unity install 6000.3.7f1 > install.log 2>&1
Exit codes
Code
Meaning
0
Success.
1
A general error occurred. Inspect stderr
for details.
130
User cancelled the command (for example with Ctrl+C or SIGINT).
Progress output
Long-running commands (such as install
) render animated progress bars on an interactive terminal and a static summary when complete. Progress output is for human readers. Don't parse it in scripts. For machine-readable results, use --format json
.
Log locations
Platform
Path
Windows %UserProfile%\AppData\Roaming\UnityHub\logs
macOS ~/Library/Application Support/UnityHub/logs
Linux ~/.config/UnityHub/logs
You can also open the log folder from the Hub: Account > Help and Support > Logs .
Migrate from the Hub CLI
If you have scripts targeting the CLI embedded in the Unity Hub desktop application (invoked with -- --headless
), the following tables summarize the behavioral and syntactic differences. For full Hub CLI syntax, refer to Hub CLI reference .
Invocation
Hub CLI
Unity CLI
How to run "Unity Hub.exe" -- --headless <command>
unity <command>
Dependency Requires the full Unity Hub desktop application. Standalone binary; no Hub installation required.
Command and flag changes
Area
Hub CLI
Unity CLI
install
version --version
/ -v <version>
(required flag) [version]
(optional positional argument)
install-modules
editor version --version
/ -v <version>
(required) -e, --editor-version <version>
(optional)
install-modules
module --module
/ -m <id>
(required) -m, --module <id>
(optional)
editors
add local Editor editors --add <path>
(flag) editors add <path...>
(command; accepts multiple paths)
-v
on install
Editor version Reserved. -V
prints the CLI version.
help
command Platform-specific help text files Replaced by --help
on every command.
Output and errors
Area
Hub CLI
Unity CLI
Default output Plain text, always human
on an interactive terminal; tsv
when piped
Structured output --json
per command (where supported) Global --format json
( --json
kept for compatibility)
Errors Written to stdout
Written to stderr
(JSON errors: {"error": "..."}
on stderr
)
Progress Plain text lines, for example downloading 23.50%
Animated progress bar; static summary on completion
Exit codes 0
success, 1
error 0
success, 1
error, 130
user cancellation
Removed global flags
These Hub CLI flags have no equivalent in the Unity CLI:
--headless
, --errors
, --silent
, --logLevel
/ -l
, --bugReporter
, --debugMode
, --inspect
, --userEmail
, --theme
, --editorLicense
, --servicesUrlInterval
, --cloudEnvironment
.
New commands
The Unity CLI adds commands not in the Hub CLI: auth
, open
, projects
, uninstall
, and upgrade
. The path shorthand unity ./MyProject
is equivalent to unity open ./MyProject
.
Impact summary
Important
Review existing scripts and continuous integration (CI) pipelines before switching. The following items describe the areas most likely to require changes.
High: scripts that fail without updates
Replace -- --headless
invocations with unity
.
Replace install -v <version>
with install <version>
(positional).
Replace install-modules --version
/ -v
with --editor-version
/ -e
.
Replace editors --add
with editors add
.
Medium: behavior changes that can produce wrong results
Piped stdout
defaults to TSV, not plain text.
Errors go to stderr
, not stdout
.
Progress output format changed. Don't parse it.
Low: additive changes that don't break existing usage
New commands: auth
, open
, projects
, uninstall
, upgrade
.
New flags such as --verbose
, --list
, and --all
.
Version aliases: latest
, lts
, default
, and short majors.
New exit code 130
for user cancellation.
Back to top
