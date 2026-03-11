// Restore original surface change to +80, and shift drawing by +40
using System;
using System.IO;
using System.Linq;
using UndertaleModLib.Compiler;

EnsureDataLoaded();

// 1. Modify oCard_Create_0
string createCode = @"surfw = sprite_get_width(sCardLayout) + 80;
surfh = sprite_get_height(sCardLayout);
surf = surface_create(surfw, surfh);
wishedFor = 0;
bw = 0;
";

// 2. Modify oCard_Draw_76 to shift drawing by +40
string drawCode = @"if (bw)
{
    shader_set(shaderBW);
}
surf = scrSurfInit(surf, surfw, surfh);
unknown = (global.cardExtra[card] + global.cardBaseAmount[card]) == 0;
draw_sprite(sCardLayout, 0, 40, 0);
if (unknown)
{
    ind = sprite_get_number(sIconCategory) - 1;
}
else
{
    ind = global.cardCategory[card];
}
draw_sprite(sIconCategory, ind, 48, 7);
scrSetText(1, 0, 1);
draw_set_colour(#E9F2F5);
if (oGameManager.metaState == 1)
{
    wishedFor = 0;
    wishType = 0;
    with (oMan)
    {
        if (wish == other.card)
        {
            other.wishedFor = 1;
            if (wishType != -1)
            {
                other.wishType = 1;
            }
        }
    }
    if (wishedFor)
    {
        draw_set_colour(#F7E243);
        if (wishType)
        {
            draw_set_colour(#D066ED);
        }
    }
}
var namex = 13 + 40;
if (global.cardCategory[card] == 4)
{
    namex = 14 + 40;
}
draw_text(namex, 5, global.cardName[card]);
draw_set_colour(c_white);
var yy = 51;
for (var i = 0; i < 2; i++)
{
    if (global.cardCost[card, i] == 0)
    {
        continue;
    }
    draw_sprite(sIconCost, i, 52, yy + 5);
    var col = 16777215;
    if (oGameManager.metaState == 1 && global.cardCost[card, i] > global.money[i])
    {
        col = 255;
    }
    draw_set_colour(col);
    draw_text(60, (yy - 2) + 5, string(global.cardCost[card, i]));
    yy += 10;
}
var _c = merge_color(global.cardColor[global.cardCategory[card]], #2B2B36, 0.5);
if (unknown)
{
    _c = 3549995;
}
draw_sprite_ext(sCardLayout, 2, 40, 0, 1, 1, 0, _c, 1);
if (unknown)
{
    ind = sprite_get_number(sIconCards) - 1;
}
else
{
    ind = card;
}
draw_sprite_ext(sIconCards, ind, 68, 30, 1, 1, 0, c_white, 1);
surface_reset_target();
if (bw)
{
    shader_reset();
}
bw = 0;
";

var importGroup = new CodeImportGroup(Data);
importGroup.QueueReplace("gml_Object_oCard_Create_0", createCode);
importGroup.QueueReplace("gml_Object_oCard_Draw_76", drawCode);
importGroup.Import();

ScriptMessage("Card surface adjusted: +80px width, +40px visual offset for perfect hitboxes!");
