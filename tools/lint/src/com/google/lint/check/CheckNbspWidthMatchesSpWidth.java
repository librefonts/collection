package com.google.lint.check;

import com.google.inject.Inject;
import com.google.lint.common.Context;
import com.google.lint.common.FamilyMetadata;
import com.google.lint.common.FontMetadata;
import com.google.lint.common.FontStore;
import com.google.lint.common.LintCheck;
import com.google.lint.common.MetadataStore;
import com.google.lint.common.Severity;
import com.google.typography.font.sfntly.Font;
import com.google.typography.font.sfntly.Tag;
import com.google.typography.font.sfntly.table.core.CMap;
import com.google.typography.font.sfntly.table.core.CMapFormat4;
import com.google.typography.font.sfntly.table.core.CMapTable;
import com.google.typography.font.sfntly.table.core.HorizontalMetricsTable;

import java.io.File;
import java.util.List;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class CheckNbspWidthMatchesSpWidth implements LintCheck {

  private static final int SP = 0x000020;
  private static final int NBSP = 0x0000A0;
  private final MetadataStore metadataStore;
  private final FontStore fontStore;

  @Inject
  public CheckNbspWidthMatchesSpWidth(MetadataStore metadataStore, FontStore fontStore) {
    this.metadataStore = metadataStore;
    this.fontStore = fontStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
        Font font = fontStore.getSfntlyFont(familyDirectory, fontMetadata);
        checkWidths(context, familyDirectory, fontMetadata, font);
      }
    }
  }

  private void checkWidths(Context context, String familyDirectory, FontMetadata fontMetadata,
      Font font) {
    CMapFormat4 cmap = retrieveCmapFormat4(font);
    if (cmap == null) {
      throw new RuntimeException("Could not find format 4 cmap in " + fontMetadata.getName());
    }
    int spGlyphId = cmap.glyphId(SP);
    int nbspGlyphId = cmap.glyphId(NBSP);
    String fontFilePath = new File(familyDirectory, fontMetadata.getFilename()).getPath();
    if (spGlyphId == CMapTable.NOTDEF) {
      context.report(Severity.ERROR, String.format("%s: The font does not contain a sp glyph",
          fontFilePath));
    }
    if (nbspGlyphId == CMapTable.NOTDEF) {
      context.report(Severity.ERROR, String.format("%s: The font does not contain a nbsp glyph",
          fontFilePath));
    }
    int spGlyphAdvanceWidth = getAdvanceWidth(spGlyphId, font);
    int nbspGlyphAdvanceWidth = getAdvanceWidth(nbspGlyphId, font);
    if (spGlyphAdvanceWidth != nbspGlyphAdvanceWidth) {
      context.report(Severity.ERROR, String.format("%s: The nbsp advance width does not match " +
            "the sp advance width", fontFilePath));
    }
  }

  private int getAdvanceWidth(int glyphId, Font font) {
    HorizontalMetricsTable hmtx = font.getTable(Tag.hmtx);
    return hmtx.advanceWidth(glyphId);
  }

  private CMapFormat4 retrieveCmapFormat4(Font font) {
    CMapTable cmapTable = font.getTable(Tag.cmap);
    for (CMap cmap : cmapTable) {
      if (cmap.format() == CMap.CMapFormat.Format4.value()) {
        return (CMapFormat4) cmap;
      }
    }
    return null;
  }
}
