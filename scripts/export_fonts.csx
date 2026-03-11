// Export font textures and glyph data for all fonts
using System;
using System.IO;
using System.Linq;
using UndertaleModLib.Util;

EnsureDataLoaded();

string outDir = @"D:\Simmiland.Build.7533614\Simmiland\cyrillic_fonts";
Directory.CreateDirectory(outDir);

using (var worker = new TextureWorker())
{
    foreach (var font in Data.Fonts)
    {
        string name = font.Name.Content;
        
        // Export font texture as PNG
        string pngPath = Path.Combine(outDir, $"{name}.png");
        worker.ExportAsPNG(font.Texture, pngPath);
        
        // Export glyph data as CSV
        string csvPath = Path.Combine(outDir, $"glyphs_{name}.csv");
        using (var writer = new StreamWriter(csvPath))
        {
            writer.WriteLine($"{font.DisplayName?.Content};{font.EmSize};{font.Bold};{font.Italic};{font.Charset};{font.AntiAliasing};{font.ScaleX};{font.ScaleY};{font.RangeStart};{font.RangeEnd}");
            foreach (var g in font.Glyphs)
            {
                writer.WriteLine($"{g.Character};{g.SourceX};{g.SourceY};{g.SourceWidth};{g.SourceHeight};{g.Shift};{g.Offset}");
            }
        }
        
        ScriptMessage($"Exported {name}: {font.Glyphs.Count} glyphs, texture saved");
    }
}

ScriptMessage($"\nAll fonts exported to {outDir}");
