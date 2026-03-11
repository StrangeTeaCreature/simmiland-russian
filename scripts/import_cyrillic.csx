// Import modified font textures with Cyrillic and update glyph data
// Uses the ImportFonts approach from UTMT

using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using UndertaleModLib;
using UndertaleModLib.Models;
using UndertaleModLib.Util;

EnsureDataLoaded();

string fontsDir = @"D:\Simmiland.Build.7533614\Simmiland\cyrillic_fonts";

int totalFontsUpdated = 0;

foreach (var font in Data.Fonts)
{
    string name = font.Name.Content;
    string pngPath = Path.Combine(fontsDir, $"{name}_cyr.png");
    string csvPath = Path.Combine(fontsDir, $"glyphs_{name}_cyr.csv");
    
    if (!File.Exists(pngPath) || !File.Exists(csvPath))
        continue;
    
    ScriptMessage($"Importing {name}...");
    
    // Read the new texture
    byte[] pngBytes = File.ReadAllBytes(pngPath);
    (int texW, int texH) = TextureWorker.GetImageSizeFromFile(pngPath);
    
    // Replace the font's texture page content
    // The font.Texture is a TexturePageItem that points to an EmbeddedTexture
    // We need to replace the EmbeddedTexture's image data
    
    // Create a new embedded texture with the modified image
    var newTexture = new UndertaleEmbeddedTexture();
    newTexture.Name = new UndertaleString($"Texture {Data.EmbeddedTextures.Count}");
    newTexture.TextureData.Image = GMImage.FromPng(pngBytes);
    Data.EmbeddedTextures.Add(newTexture);
    
    // Create a new texture page item pointing to the new texture
    var newTexPageItem = new UndertaleTexturePageItem()
    {
        Name = new UndertaleString($"PageItem {Data.TexturePageItems.Count}"),
        TexturePage = newTexture,
        SourceX = 0,
        SourceY = 0,
        SourceWidth = (ushort)texW,
        SourceHeight = (ushort)texH,
        TargetX = 0,
        TargetY = 0,
        TargetWidth = (ushort)texW,
        TargetHeight = (ushort)texH,
        BoundingWidth = (ushort)texW,
        BoundingHeight = (ushort)texH
    };
    Data.TexturePageItems.Add(newTexPageItem);
    
    // Update font to use the new texture page item
    font.Texture = newTexPageItem;
    
    // Read new glyph data from CSV
    string[] csvLines = File.ReadAllLines(csvPath);
    
    // Clear existing glyphs and add all from CSV
    font.Glyphs.Clear();
    
    for (int i = 1; i < csvLines.Length; i++)
    {
        string line = csvLines[i].Trim();
        if (string.IsNullOrEmpty(line)) continue;
        
        string[] parts = line.Split(';');
        if (parts.Length < 7) continue;
        
        var glyph = new UndertaleFont.Glyph()
        {
            Character = ushort.Parse(parts[0]),
            SourceX = ushort.Parse(parts[1]),
            SourceY = ushort.Parse(parts[2]),
            SourceWidth = ushort.Parse(parts[3]),
            SourceHeight = ushort.Parse(parts[4]),
            Shift = short.Parse(parts[5]),
            Offset = short.Parse(parts[6]),
        };
        
        font.Glyphs.Add(glyph);
    }
    
    // Sort glyphs
    var sorted = font.Glyphs.OrderBy(g => g.Character).ToList();
    font.Glyphs.Clear();
    foreach (var g in sorted)
        font.Glyphs.Add(g);
    
    // Update range to include Cyrillic
    if (font.RangeEnd < 0x0451)
        font.RangeEnd = 0x0451;
    
    int cyrCount = font.Glyphs.Count(g => g.Character >= 0x0400 && g.Character <= 0x04FF);
    ScriptMessage($"  {name}: {font.Glyphs.Count} total glyphs ({cyrCount} Cyrillic), texture {texW}x{texH}");
    totalFontsUpdated++;
}

ScriptMessage($"\nUpdated {totalFontsUpdated} fonts with Cyrillic support!");
ScriptMessage("Save the file to apply changes.");
