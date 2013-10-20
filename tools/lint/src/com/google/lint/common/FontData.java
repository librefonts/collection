package com.google.lint.common;

import com.google.common.base.Objects;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class FontData {

  private final FontMetadata fontMetadata;
  private final byte[] fontData;

  public FontData(FontMetadata fontMetadata, byte[] fontData) {
    this.fontMetadata = fontMetadata;
    this.fontData = fontData;
  }

  public byte[] getBytes() {
    return fontData;
  }

  public String getName() {
    return fontMetadata.getName();
  }

  public String getFilename() {
    return fontMetadata.getFilename();
  }

  @Override
  public boolean equals(Object obj) {
    if (!(obj instanceof FontData)) {
      return false;
    }
    FontData otherFontData = (FontData) obj;
    return Objects.equal(fontMetadata, otherFontData.fontMetadata) &&
        Objects.equal(fontData, otherFontData.fontData);
  }

  @Override
  public int hashCode() {
    return Objects.hashCode(fontMetadata, fontData);
  }
}
