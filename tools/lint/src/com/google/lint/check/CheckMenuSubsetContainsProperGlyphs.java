package com.google.lint.check;

import com.google.common.base.Joiner;
import com.google.common.collect.Sets;
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

import java.io.File;
import java.util.List;
import java.util.Set;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class CheckMenuSubsetContainsProperGlyphs implements LintCheck {

  private final MetadataStore metadataStore;
  private final FontStore fontStore;

  @Inject
  public CheckMenuSubsetContainsProperGlyphs(MetadataStore metadataStore, FontStore fontStore) {
    this.metadataStore = metadataStore;
    this.fontStore = fontStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
        File menuFile = new File(familyDirectory,
            fontMetadata.getFilename().replace(".ttf", ".menu"));
        if (menuFile.exists()) {
          Font font = fontStore.getSfntlyFont(familyDirectory, fontMetadata, "menu");
          checkContainsProperGlyph(context, familyDirectory, fontMetadata, font);
        }
      }
    }
  }

  private void checkContainsProperGlyph(
      Context context, String familyDirectory, FontMetadata fontMetadata, Font font) {
    CMapFormat4 cmap = retrieveCmapFormat4(font);
    Set<String> missingGlyphs = Sets.newHashSet();
    String familyName = fontMetadata.getName();

    if (cmap.glyphId(" ".codePointAt(0)) == CMapTable.NOTDEF) {
      missingGlyphs.add(" ");
    }
    for (int i = 0; i < familyName.length(); i++) {
      if (cmap.glyphId(familyName.codePointAt(i)) == CMapTable.NOTDEF) {
        missingGlyphs.add(familyName.substring(i, i + 1));
      }
    }
    if (!missingGlyphs.isEmpty()) {
      String filePath = new File(familyDirectory, fontMetadata.getFilename()).getPath();
      context.report(Severity.ERROR, String.format(
          "%s: Menu is missing glyphs: \"%s\"", filePath, Joiner.on("").join(missingGlyphs)));
    }
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
