// Drop this anywhere under an Editor assembly in your Unity project.
// Every static method tagged with [CliCommand] becomes a `unity command <name>` tool.
// No registration step, no MCP config.
//
//   unity command validate_content --strict true --project-path <project>
//   unity command spawn_marker --name Waypoint --x 0 --y 1 --z 0 --project-path <project>

using UnityEngine;
using Unity.Pipeline.Commands;

public static class MyPipelineCommands
{
    // Returns a non-zero exit code so CI can gate on it.
    [CliCommand("validate_content", "Validate all content definitions")]
    public static int ValidateContent(
        [CliArg("strict", "Fail on warnings, not just errors")] bool strict = false)
    {
        var warnings = 0;
        var errors = 0;

        // ... walk your ScriptableObjects / assets here and count problems ...

        Debug.Log($"[validate_content] errors={errors} warnings={warnings}");

        if (errors > 0) return 1;
        if (strict && warnings > 0) return 1;
        return 0;
    }

    // Runs on the Editor main thread, so engine APIs are safe to touch.
    [CliCommand("spawn_marker", "Create a marker GameObject at a position")]
    [MainThreadRequired]
    public static string SpawnMarker(
        [CliArg("name", "GameObject name")] string name = "Marker",
        [CliArg("x", "World X")] float x = 0f,
        [CliArg("y", "World Y")] float y = 0f,
        [CliArg("z", "World Z")] float z = 0f)
    {
        var go = new GameObject(name);
        go.transform.position = new Vector3(x, y, z);
        return $"created {name} at ({x}, {y}, {z})";
    }
}
