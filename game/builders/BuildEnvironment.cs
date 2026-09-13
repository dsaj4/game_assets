using Godot;

// Build-time environment fixture only. No game or UI content.
public partial class BuildEnvironment : SceneTree
{
    public override void _Initialize()
    {
        var root = new Node3D { Name = "EnvironmentOnly" };
        var scene = new PackedScene();
        if (scene.Pack(root) != Error.Ok) { Quit(1); return; }
        var instance = scene.Instantiate();
        bool valid = instance is Node3D && instance.GetChildCount() == 0;
        instance.Free();
        var result = valid ? ResourceSaver.Save(scene, "res://scenes/EnvironmentOnly.tscn") : Error.Failed;
        root.Free();
        GD.Print($"ENVIRONMENT_SCENE_BUILD={result}");
        Quit(result == Error.Ok ? 0 : 1);
    }
}
