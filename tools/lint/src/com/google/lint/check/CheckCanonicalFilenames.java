package com.google.lint.check;

import com.google.common.base.Strings;
import com.google.common.collect.ImmutableMap;
import com.google.inject.Inject;
import com.google.lint.common.Context;
import com.google.lint.common.FamilyMetadata;
import com.google.lint.common.FontMetadata;
import com.google.lint.common.LintCheck;
import com.google.lint.common.MetadataStore;
import com.google.lint.common.Severity;

import java.io.File;
import java.util.List;
import java.util.Map;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class CheckCanonicalFilenames implements LintCheck {

  private static final Map<Integer, String> weightNames = ImmutableMap.<Integer, String>builder()
      .put(100, "Thin")
      .put(200, "ExtraLight")
      .put(300, "Light")
      .put(400, "")
      .put(500, "Medium")
      .put(600, "SemiBold")
      .put(700, "Bold")
      .put(800, "ExtraBold")
      .put(900, "Black")
      .build();
  private static final Map<String, String> styleNames = ImmutableMap.<String, String>builder()
      .put("normal", "")
      .put("italic", "Italic")
      .build();
  private final MetadataStore metadataStore;

  @Inject
  public CheckCanonicalFilenames(MetadataStore metadataStore) {
    this.metadataStore = metadataStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
        String canonicalFileName = createCanonicalFilename(fontMetadata);
        if (!canonicalFileName.equals(fontMetadata.getFilename())) {
          String filePath = new File(familyDirectory, fontMetadata.getFilename()).getPath();
          context.report(Severity.WARNING, String.format("%s: Filename should be %s but is %s",
              filePath, canonicalFileName, fontMetadata.getFilename()));
        }
      }
    }
  }

  private String createCanonicalFilename(FontMetadata fontMetadata) {
    String familyName = fontMetadata.getName().replaceAll(" ", "");
    String styleWeight = String.format("%s%s", weightNames.get(fontMetadata.getWeight()),
        styleNames.get(fontMetadata.getStyle()));
    if (Strings.isNullOrEmpty(styleWeight)) {
      styleWeight = "Regular";
    }
    return String.format("%s-%s.ttf", familyName, styleWeight);
  }
}
