package com.google.lint.common;

import com.google.common.base.Objects;

import java.util.List;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class FamilyMetadata {

  private String name;
  private String designer;
  private String license; // Create enum
  private String visibility; // Create enum, check that it is a valid visibility
  private String category;
  private int size;
  private List<FontMetadata> fonts;
  private List<String> subsets; // Create enum?
  private String dateAdded; // use DateTime?

  public String getName() {
    return name;
  }

  public List<FontMetadata> getFontsMetadata() {
    return fonts;
  }

  public List<String> getSubsets() {
    return subsets;
  }

  @Override
  public boolean equals(Object obj) {
    if (!(obj instanceof FamilyMetadata)) {
      return false;
    }
    FamilyMetadata otherFamilyMetadata = (FamilyMetadata) obj;
    return Objects.equal(name, otherFamilyMetadata.name) &&
        Objects.equal(designer, otherFamilyMetadata.designer) &&
        Objects.equal(license, otherFamilyMetadata.license) &&
        Objects.equal(visibility, otherFamilyMetadata.visibility) &&
        Objects.equal(category, otherFamilyMetadata.category) &&
        Objects.equal(size, otherFamilyMetadata.size) &&
        Objects.equal(fonts, otherFamilyMetadata.fonts) &&
        Objects.equal(subsets, otherFamilyMetadata.subsets) &&
        Objects.equal(dateAdded, otherFamilyMetadata.dateAdded);
  }

  @Override
  public int hashCode() {
    return Objects.hashCode(name, designer, license, visibility, category, size, fonts, subsets,
        dateAdded);
  }
}
