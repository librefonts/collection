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
import com.google.typography.font.sfntly.table.core.NameTable;
import com.google.typography.font.sfntly.table.core.NameTable.NameId;

import java.io.File;
import java.util.List;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class CheckMetadataMatchesNameTable implements LintCheck {

  private final MetadataStore metadataStore;
  private final FontStore fontStore;

  @Inject
  public CheckMetadataMatchesNameTable(MetadataStore metadataStore, FontStore fontStore) {
    this.metadataStore = metadataStore;
    this.fontStore = fontStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      checkFamilyNameMatchesNameTable(context, familyDirectory, familyMetadata);
    }
  }

  private void checkFamilyNameMatchesNameTable(Context context, String familyDirectory,
      FamilyMetadata familyMetadata) {
    String familyName = familyMetadata.getName();
    for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
      Font font = fontStore.getSfntlyFont(familyDirectory, fontMetadata);
      String familyNameFromFont = extractNameFromNameTable(font);
      if (!familyName.equals(familyNameFromFont)) {
        String report = String.format("%s: Family name was supposed to be \"%s\" but is \"%s\"",
            new File(familyDirectory, fontMetadata.getFilename()).getPath(), familyName,
            familyNameFromFont);
        context.report(Severity.ERROR, report);
      }
    }
  }

  private String extractNameFromNameTable(Font font) {
    NameTable nameTable = font.getTable(Tag.name);
    NameId nameId = NameId.FontFamilyName;
    String value = nameTable.name(Font.PlatformId.Macintosh.value(),
        Font.UnicodeEncodingId.Unicode1_0.value(),
        NameTable.MacintoshLanguageId.English.value(), nameId.value());
    if (value != null) {
      return value;
    }
    return nameTable.name(Font.PlatformId.Windows.value(),
        Font.WindowsEncodingId.UnicodeUCS2.value(),
        NameTable.WindowsLanguageId.English_UnitedStates.value(), nameId.value());
  }
}
