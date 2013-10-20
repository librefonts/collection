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
import com.google.typography.font.sfntly.table.core.OS2Table;

import java.io.File;
import java.util.List;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class CheckCanonicalWeights implements LintCheck {

  private final MetadataStore metadataStore;
  private final FontStore fontStore;

  @Inject
  public CheckCanonicalWeights(MetadataStore metadataStore, FontStore fontStore) {
    this.metadataStore = metadataStore;
    this.fontStore = fontStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
        checkWeight(context, familyDirectory, fontMetadata);
        checkOverwrite(context, familyDirectory, fontMetadata);
      }
    }
  }

  private void checkOverwrite(Context context, String familyDirectory, FontMetadata fontMetadata) {
    String filePath = new File(familyDirectory, fontMetadata.getFilename()).getPath();
    Font font = fontStore.getSfntlyFont(familyDirectory, fontMetadata);
    OS2Table os2Table = font.getTable(Tag.OS_2);
    if (fontMetadata.getWeight() != os2Table.usWeightClass()) {
      context.report(Severity.WARNING, String.format("%s: METADATA.json overwrites the weight. " +
          "The METADATA.json weight is %d and the font file %s weight is %d", filePath,
          fontMetadata.getWeight(), fontMetadata.getFilename(), os2Table.usWeightClass()));
    }
  }

  private void checkWeight(Context context, String familyDirectory, FontMetadata fontMetadata) {
    int weight = fontMetadata.getWeight();
    int firstDigit = weight / 100;
    if ((weight % 100) != 0 || (firstDigit < 1 || firstDigit > 9)) {
      context.report(Severity.ERROR, String.format("%s: The weight is %d which is not a " +
          "multiple of 100 between 1 and 9",
          new File(familyDirectory, "METADATA.json").getPath(), weight));
    }
  }
}
