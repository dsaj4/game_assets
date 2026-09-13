using Godot;
using System;

// Godogen-style build-time scene emission. Imported GLB internals remain instanced.
public partial class BuildE1 : SceneTree
{
    static int Count(Node node)
    {
        int n = 1;
        foreach (Node child in node.GetChildren()) n += Count(child);
        return n;
    }
    static void Own(Node node, Node root)
    {
        foreach (Node child in node.GetChildren())
        {
            child.Owner = root;
            if (string.IsNullOrEmpty(child.SceneFilePath)) Own(child, root);
        }
    }
    public override void _Initialize()
    {
        try
        {
            foreach (string variant in new[] { "base", "ink" })
            {
                var root = new Node3D { Name = variant == "ink" ? "E1Ink" : "E1Base" };
                var model = GD.Load<PackedScene>($"res://assets/e1/e1_{variant}.glb").Instantiate<Node3D>();
                model.Name = "Specimen";
                root.AddChild(model);
                root.AddChild(new WorldEnvironment
                {
                    Name = "PaperLight",
                    Environment = new Godot.Environment
                    {
                        BackgroundMode = Godot.Environment.BGMode.Color,
                        BackgroundColor = new Color("19201b"),
                        AmbientLightSource = Godot.Environment.AmbientSource.Color,
                        AmbientLightColor = new Color("d2d9cc"),
                        AmbientLightEnergy = 0.58f,
                        TonemapMode = Godot.Environment.ToneMapper.Linear,
                        SsaoEnabled = true,
                        SsaoRadius = 0.35f,
                        SsaoIntensity = 1.15f
                    }
                });
                root.AddChild(new DirectionalLight3D
                {
                    Name = "BroadKey", RotationDegrees = new Vector3(-65, -28, 0),
                    LightColor = new Color("f2f0e3"), LightEnergy = 0.78f,
                    ShadowEnabled = true, DirectionalShadowMaxDistance = 40
                });
                root.AddChild(new CanvasLayer { Name = "Labels" });
                Own(root, root);
                int expected = Count(root);
                // SetScript invalidates the original managed wrapper; refetch before packing.
                var holder = new Node(); holder.AddChild(root);
                root.SetScript(GD.Load<Script>("res://scripts/E1View.cs"));
                var packRoot = holder.GetChild(0);
                var packed = new PackedScene();
                if (packed.Pack(packRoot) != Error.Ok) throw new Exception("Pack failed");
                var reloaded = packed.Instantiate(); int actual = Count(reloaded); reloaded.Free();
                if (expected != actual) throw new Exception($"Node loss: {expected} != {actual}");
                var error = ResourceSaver.Save(packed, $"res://scenes/E1{(variant == "ink" ? "Ink" : "Base")}.tscn");
                if (error != Error.Ok) throw new Exception(error.ToString());
                GD.Print($"E1_PACK_{variant}=PASS nodes_before={expected} nodes_after={actual}");
                holder.Free();
            }
            Quit(0);
        }
        catch (Exception e) { GD.PushError(e.ToString()); Quit(1); }
    }
}
