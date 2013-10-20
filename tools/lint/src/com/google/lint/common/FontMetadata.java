package com.google.lint.common;

import com.google.common.base.Objects;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class FontMetadata {

  private String name;
  private String style;
  private int weight;
  private String filename;
  private String postScriptName;
  private String fullName;
  private String copyright;

  public String getName() {
    return name;
  }

  public String getStyle() {
    return style;
  }

  public int getWeight() {
    return weight;
  }

  public String getFilename() {
    return filename;
  }

  @Override
  public boolean equals(Object obj) {
    if (!(obj instanceof FontMetadata)) {
      return false;
    }
    FontMetadata otherFontMetadata = (FontMetadata) obj;
    return Objects.equal(name, otherFontMetadata.name) &&
        Objects.equal(style, otherFontMetadata.style) &&
        Objects.equal(weight, otherFontMetadata.weight) &&
        Objects.equal(filename, otherFontMetadata.filename) &&
        Objects.equal(postScriptName, otherFontMetadata.postScriptName) &&
        Objects.equal(fullName, otherFontMetadata.fullName) &&
        Objects.equal(copyright, otherFontMetadata.copyright);
  }

  @Override
  public int hashCode() {
    return Objects.hashCode(name, style, weight, filename, postScriptName, fullName, copyright);
  }
}
