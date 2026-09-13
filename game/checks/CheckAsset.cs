using Godot;

// Checks a temporary Blender export outside runtime assets.
public partial class CheckAsset : SceneTree
{
    public override void _Initialize()
    {
        var state = new GltfState();
        var document = new GltfDocument();
        var path = ProjectSettings.GlobalizePath("res://../artifacts/environment-smoke/cube.glb");
        var error = document.AppendFromFile(path, state);
        var scene = error == Error.Ok ? document.GenerateScene(state) : null;
        bool valid = scene != null && scene.FindChildren("*", "MeshInstance3D", true, false).Count > 0;
        scene?.Free();
        GD.Print($"BLENDER_GLB_LOAD={(valid ? "PASS" : "FAIL")}");
        Quit(valid ? 0 : 1);
    }
}
