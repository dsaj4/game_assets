using Godot;
using System;
using System.Collections.Generic;

// E1 review controls only: no inventory, spell logic or route navigation.
public partial class E1View : Node3D
{
    Camera3D camera = null!;
    CanvasLayer canvas = null!;
    // Local review fonts only: no operating-system font files are redistributed.
    readonly SystemFont font = new() { FontNames = new[] { "KaiTi", "SimSun", "Microsoft YaHei" } };
    readonly SystemFont utilityFont = new() { FontNames = new[] { "Microsoft YaHei", "Noto Sans CJK SC" } };
    readonly List<(Label label, Node3D anchor, Vector2 size, Panel? plaque)> anchored = new();
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
            ScreenText("言咒 · 工匠台", new Vector2(88, 24), new Vector2(800, 58), 42, "dfdfc7");
            ScreenText("法杖与行图", new Vector2(1360, 34), new Vector2(480, 42), 26, "a8b09c", HorizontalAlignment.Right);
            ScreenText("一杖一咒 · 临行整备", new Vector2(92, 93), new Vector2(600, 34), 23, "aeb39c");
            AnchorText("TagAcquireText", "获得", 44, "26392a", new Vector2(180, 64));
            AnchorText("TagArmorText", "护甲", 44, "2d3629", new Vector2(180, 64));
            AnchorText("MapTitle", "远 行 图", 36, "30382a", new Vector2(300, 54));
            AnchorText("MapCaption", "群山之间 · 旧塔图记", 23, "48503c", new Vector2(440, 42));
            AnchorText("EncounterCaption", "塔楼", 28, "303b28", new Vector2(230, 46));
            AnchorText("InlayCaption", "固定镶嵌 · 翡翠", 24, "354232", new Vector2(222, 40), plaque: true);
            AnchorText("WandCaption", "一杖 · 一咒\n木胎 / 铜箍 / 翡翠", 26, "303b2d", new Vector2(350, 86), plaque: true);
            ScreenText("材质审阅   [1] 基础   [2] 墨线   [Esc] 退出", new Vector2(90, 1000), new Vector2(1200, 40), 22, "aab09e", utility: true);
            ScreenText(ink ? "E1 修订小样 · B 墨线" : "E1 修订小样 · A 基础", new Vector2(1400, 1000), new Vector2(430, 40), 22, "aab09e", HorizontalAlignment.Right, utility: true);
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
    Label MakeLabel(string text, Vector2 size, int fontSize, string color, bool utility = false)
    {
        var selectedFont = utility ? utilityFont : font;
        var label = new Label
        {
            Text = text, HorizontalAlignment = HorizontalAlignment.Center,
            VerticalAlignment = VerticalAlignment.Center, MouseFilter = Control.MouseFilterEnum.Ignore
        };
        label.AddThemeFontOverride("font", selectedFont);
        label.AddThemeFontSizeOverride("font_size", Math.Max(16, Mathf.RoundToInt(fontSize * scale)));
        label.AddThemeColorOverride("font_color", new Color(color));
        canvas.AddChild(label);
        label.Size = size * scale;
        foreach (char c in text)
            if (!char.IsWhiteSpace(c) && !selectedFont.HasChar(c)) throw new Exception($"Missing font glyph: {c}");
        return label;
    }
    void ScreenText(string text, Vector2 position, Vector2 size, int fontSize, string color, HorizontalAlignment align = HorizontalAlignment.Left, bool utility = false)
    {
        var label = MakeLabel(text, size, fontSize, color, utility); label.Position = position * scale;
        label.HorizontalAlignment = align; overlays.Add(label);
    }
    void AnchorText(string name, string text, int fontSize, string color, Vector2 size, bool plaque = false)
    {
        var anchor = GetNode("Specimen").FindChild(name, true, false) as Node3D
            ?? throw new Exception($"Missing text anchor: {name}");
        Panel? backing = null;
        if (plaque)
        {
            // A small, quiet label surface protects text from the wood's hatch marks.
            // Keep the specimen visible; these plates cover only their own captions.
            backing = new Panel { MouseFilter = Control.MouseFilterEnum.Ignore };
            backing.AddThemeStyleboxOverride("panel", new StyleBoxFlat
            {
                BgColor = new Color("c8cbb3"), BorderColor = new Color("545b47"),
                BorderWidthLeft = 1, BorderWidthRight = 1,
                BorderWidthTop = 1, BorderWidthBottom = 1,
                ShadowColor = new Color(0.04f, 0.07f, 0.04f, 0.35f), ShadowSize = 3
            });
            canvas.AddChild(backing);
        }
        anchored.Add((MakeLabel(text, size, fontSize, color), anchor, size, backing));
    }
    void LayoutAndValidate()
    {
        var viewport = GetViewport().GetVisibleRect();
        foreach (var entry in anchored)
        {
            entry.label.Position = camera.UnprojectPosition(entry.anchor.GlobalPosition) - entry.size * scale / 2;
            if (entry.plaque != null)
            {
                entry.plaque.Position = entry.label.Position - new Vector2(12, 5) * scale;
                entry.plaque.Size = (entry.size + new Vector2(24, 10)) * scale;
                if (!viewport.Encloses(entry.plaque.GetRect())) throw new Exception("Caption plaque outside viewport");
            }
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
