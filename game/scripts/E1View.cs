using Godot;
using System;
using System.Collections.Generic;

// E1 review controls only: no inventory, spell logic or route navigation.
public partial class E1View : Node3D
{
    Camera3D camera = null!;
    CanvasLayer canvas = null!;
    readonly SystemFont font = new() { FontNames = new[] { "Microsoft YaHei", "Noto Sans CJK SC" } };
    readonly List<(Label label, Node3D anchor, Vector2 size)> anchored = new();
    readonly List<Control> overlays = new();
    float scale;

    public override async void _Ready()
    {
        try
        {
            // Wait for the native window's viewport to settle before projecting labels.
            await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
            camera = GetNode("Specimen").FindChild("E1Camera", true, false) as Camera3D
                ?? throw new Exception("Missing exported camera");
            camera.Current = true;
            // Blender orthographic width. Keep it invariant at both capture resolutions.
            camera.KeepAspect = Camera3D.KeepAspectEnum.Width; camera.Size = 18.6f;
            if (DisplayServer.GetName() == "headless")
            {
                GD.Print("E1_HEADLESS_ASSET=PASS UI checks require native viewport");
                return;
            }
            canvas = GetNode<CanvasLayer>("Labels");
            scale = GetViewport().GetVisibleRect().Size.X / 1920f;
            bool ink = Name.ToString().Contains("Ink");
            ScreenText("言咒  /  风格样本", new Vector2(88, 26), new Vector2(800, 52), 34, "e0d5aa");
            ScreenText("E1   ·   原生 3D / 固定机位", new Vector2(1220, 33), new Vector2(620, 42), 24, "a5b19c", HorizontalAlignment.Right);
            ScreenText(ink ? "B  墨线材质" : "A  基础材质", new Vector2(90, 96), new Vector2(500, 38), 23, "d9c898");
            AnchorText("TagAcquireText", "获得", 40, "25392a", new Vector2(180, 64));
            AnchorText("TagArmorText", "护甲", 40, "303427", new Vector2(180, 64));
            AnchorText("MapTitle", "远 行 图", 32, "383d2d", new Vector2(300, 50));
            AnchorText("MapCaption", "纸面地形  ·  单节点摆件", 22, "444737", new Vector2(440, 42));
            AnchorText("EncounterCaption", "遭遇 · 塔楼", 25, "353d2a", new Vector2(230, 43));
            AnchorText("InlayCaption", "↑ 固定镶嵌", 22, "b5c497", new Vector2(230, 42));
            AnchorText("WandCaption", "一条法术 · 一根法杖\n木胎 / 黄铜 / 翡翠", 26, "d7d0ad", new Vector2(510, 95));
            ScreenText("材质对照：  [1] 基础    [2] 墨线     [Esc] 退出", new Vector2(90, 1000), new Vector2(1250, 40), 23, "b5bea8");
            ScreenText("E1 / 样本 01", new Vector2(1460, 1000), new Vector2(370, 40), 23, "b5bea8", HorizontalAlignment.Right);
            LayoutAndValidate();
            GD.Print($"E1_READY variant={(ink ? "ink" : "base")} viewport={GetViewport().GetVisibleRect().Size} camera={camera.GlobalTransform} font={font.GetFontName()} anchors={anchored.Count}");
            var args = OS.GetCmdlineUserArgs();
            for (int i = 0; i < args.Length - 1; i++)
            {
                if (args[i] != "--capture") continue;
                // Read the actual native GPU viewport, avoiding movie-writer output scaling.
                for (int frame = 0; frame < 4; frame++)
                    await ToSignal(RenderingServer.Singleton, RenderingServer.SignalName.FramePostDraw);
                using var image = GetViewport().GetTexture().GetImage();
                var error = image.SavePng(args[i + 1]);
                if (error != Error.Ok) throw new Exception($"PNG save failed: {error}");
                GD.Print($"E1_CAPTURE_SAVED={image.GetWidth()}x{image.GetHeight()} path={args[i + 1]}");
                GetTree().Quit();
                break;
            }
        }
        catch (Exception e) { GD.PushError(e.ToString()); GetTree().Quit(1); }
    }
    Label MakeLabel(string text, Vector2 size, int fontSize, string color)
    {
        var label = new Label
        {
            Text = text, HorizontalAlignment = HorizontalAlignment.Center,
            VerticalAlignment = VerticalAlignment.Center, MouseFilter = Control.MouseFilterEnum.Ignore
        };
        label.AddThemeFontOverride("font", font);
        label.AddThemeFontSizeOverride("font_size", Math.Max(16, Mathf.RoundToInt(fontSize * scale)));
        label.AddThemeColorOverride("font_color", new Color(color));
        canvas.AddChild(label);
        label.Size = size * scale;
        foreach (char c in text)
            if (!char.IsWhiteSpace(c) && !font.HasChar(c)) throw new Exception($"Missing font glyph: {c}");
        return label;
    }
    void ScreenText(string text, Vector2 position, Vector2 size, int fontSize, string color, HorizontalAlignment align = HorizontalAlignment.Left)
    {
        var label = MakeLabel(text, size, fontSize, color); label.Position = position * scale;
        label.HorizontalAlignment = align; overlays.Add(label);
    }
    void AnchorText(string name, string text, int fontSize, string color, Vector2 size)
    {
        var anchor = GetNode("Specimen").FindChild(name, true, false) as Node3D
            ?? throw new Exception($"Missing text anchor: {name}");
        anchored.Add((MakeLabel(text, size, fontSize, color), anchor, size));
    }
    void LayoutAndValidate()
    {
        var viewport = GetViewport().GetVisibleRect();
        foreach (var entry in anchored)
        {
            entry.label.Position = camera.UnprojectPosition(entry.anchor.GlobalPosition) - entry.size * scale / 2;
            if (!viewport.Encloses(entry.label.GetRect())) throw new Exception($"Label outside viewport: {entry.label.Text} rect={entry.label.GetRect()} viewport={viewport} anchor={entry.anchor.GlobalPosition} camera={camera.GlobalTransform}");
            if (entry.label.GetMinimumSize().X > entry.size.X * scale + 1) throw new Exception("Label width overflow");
        }
        foreach (Control control in overlays)
            if (!viewport.Encloses(control.GetRect())) throw new Exception("Overlay outside viewport");
        GD.Print("E1_TEXT_BOUNDS=PASS glyphs=PASS");
    }
    public override void _UnhandledKeyInput(InputEvent @event)
    {
        if (@event is not InputEventKey key || !key.Pressed || key.Echo) return;
        if (key.Keycode == Key.Key1) GetTree().ChangeSceneToFile("res://scenes/E1Base.tscn");
        if (key.Keycode == Key.Key2) GetTree().ChangeSceneToFile("res://scenes/E1Ink.tscn");
        if (key.Keycode == Key.Escape) GetTree().Quit();
    }
}
