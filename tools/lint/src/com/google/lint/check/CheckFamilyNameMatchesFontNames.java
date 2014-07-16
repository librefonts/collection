package com.google.lint.check;

import com.google.inject.Inject;
import com.google.lint.common.Context;
import com.google.lint.common.FamilyMetadata;
import com.google.lint.common.FontMetadata;
import com.google.lint.common.LintCheck;
import com.google.lint.common.MetadataStore;
import com.google.lint.common.Severity;

import java.io.File;
import java.util.List;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class CheckFamilyNameMatchesFontNames implements LintCheck {

  private final MetadataStore metadataStore;

  @Inject
  public CheckFamilyNameMatchesFontNames(MetadataStore metadataStore) {
    this.metadataStore = metadataStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      String familyName = familyMetadata.getName();
      for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
        String fontName = fontMetadata.getName();
        if (!familyName.equals(fontName)) {
          String report = String.format("%s: Family name \"%s\" does not match font name: \"%s\"",
              new File(familyDirectory, "METADATA.json").getPath(), familyName,
              fontName);
          context.report(Severity.ERROR, report);
        }
      }
    }
  }
}
