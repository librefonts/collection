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
public class CheckSubsetsExist implements LintCheck {

  private final MetadataStore metadataStore;

  @Inject
  public CheckSubsetsExist(MetadataStore metadataStore) {
    this.metadataStore = metadataStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      checkSubsetsExist(context, familyDirectory, familyMetadata);
    }
  }

  private void checkSubsetsExist(
      Context context, String familyDirectory, FamilyMetadata familyMetadata) {
    for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
      for (String subset : familyMetadata.getSubsets()) {
        String subsetFilename = fontMetadata.getFilename().replace(".ttf", "." + subset);
        File subsetFile = new File(familyDirectory, subsetFilename);
        if (!subsetFile.exists()) {
          context.report(Severity.ERROR, String.format("%s: The subset file for the %s subset" +
              " does not exist", subsetFile.getPath(), subset));
        } else {
          File originalTtf = new File(familyDirectory, fontMetadata.getFilename());
          if (subsetFile.length() > originalTtf.length()) {
            context.report(Severity.ERROR, String.format("%s: The subset file %s is bigger than " +
                "the original file %s", subsetFile.getPath(), subsetFilename,
                fontMetadata.getFilename()));
          }
        }
      }
    }
  }
}
