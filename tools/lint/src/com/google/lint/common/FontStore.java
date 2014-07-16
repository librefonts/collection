package com.google.lint.common;

import com.google.common.collect.Maps;
import com.google.common.io.Files;
import com.google.typography.font.sfntly.Font;
import com.google.typography.font.sfntly.FontFactory;

import java.io.File;
import java.io.IOException;
import java.util.Map;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class FontStore {

  private static final FontFactory FONT_FACTORY = getFontFactory();

  private static FontFactory getFontFactory() {
    FontFactory fontFactory = FontFactory.getInstance();
    fontFactory.fingerprintFont(false);
    return fontFactory;
  }

  private final Map<String, FontData> fontsData = Maps.newHashMap();
  private final Map<FontData, Font> sfntlyFonts = Maps.newHashMap();
  private final Map<String, Font> subsets = Maps.newHashMap();

  public FontData getFontData(String familyDirectory, FontMetadata fontMetadata) {
    String filePath = createFilePath(familyDirectory, fontMetadata);
    FontData fontData = fontsData.get(filePath);
    if (fontData == null) {
      fontData = loadFont(filePath, fontMetadata);
      fontsData.put(filePath, fontData);
    }
    return fontData;
  }

  public Font getSfntlyFont(String familyDirectory, FontMetadata fontMetadata, String subset) {
    String subsetFilename = fontMetadata.getFilename().replace(".ttf", "." + subset);
    Font font = subsets.get(subsetFilename);
    if (font == null) {
      font = loadSubset(familyDirectory, subsetFilename);
      subsets.put(subsetFilename, font);
    }
    return font;
  }

  private Font loadSubset(String familyDirectory, String subsetFilename) {
    File filePath = new File(familyDirectory, subsetFilename);
    try {
      return parse(filePath.getName(), Files.toByteArray(filePath));
    } catch (IOException e) {
      throw new RuntimeException(String.format("Could not load subset file: %s", filePath), e);
    }
  }

  public Font getSfntlyFont(String familyDirectory, FontMetadata fontMetadata) {
    return getSfntlyFont(getFontData(familyDirectory, fontMetadata));
  }

  public Font getSfntlyFont(FontData fontData) {
    Font sfntlyFont = sfntlyFonts.get(fontData);
    if (sfntlyFont == null) {
      sfntlyFont = parse(fontData);
      sfntlyFonts.put(fontData, sfntlyFont);
    }
    return sfntlyFont;
  }

  private Font parse(FontData fontData) {
    return parse(fontData.getFilename(), fontData.getBytes());
  }

  private Font parse(String filename, byte[] bytes) {
    try {
      return FONT_FACTORY.loadFonts(bytes)[0];
    } catch (IOException e) {
      throw new RuntimeException(String.format("Could not parse font: %s", filename), e);
    }
  }

  private FontData loadFont(String filePath, FontMetadata fontMetadata) {
    try {
      return new FontData(fontMetadata, Files.toByteArray(new File(filePath)));
    } catch (IOException e) {
      throw new RuntimeException(String.format("Could not load font file: %s", filePath), e);
    }
  }

  private String createFilePath(String familyDirectory, FontMetadata fontMetadata) {
    return new File(familyDirectory, fontMetadata.getFilename()).getPath();
  }
}
