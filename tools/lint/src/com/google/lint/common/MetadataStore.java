package com.google.lint.common;

import com.google.common.collect.Maps;
import com.google.common.io.Files;
import com.google.gson.Gson;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.Map;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class MetadataStore {

  private static final String METADATA_JSON = "METADATA.json";
  private static final Gson gson = new Gson();

  private final Map<String, FamilyMetadata> familiesMetadata = Maps.newHashMap();

  public FamilyMetadata getFamilyMetadata(String path) {
    FamilyMetadata familyMetadata = familiesMetadata.get(path);
    if (familyMetadata == null) {
      familyMetadata = parse(path);
      familiesMetadata.put(path, familyMetadata);
    }
    return familyMetadata;
  }

  private FamilyMetadata parse(String path) {
    File metadataFile = new File(path, METADATA_JSON);
    String json;
    try {
      json = Files.toString(metadataFile, Charset.forName("UTF-8"));
    } catch (IOException e) {
      throw new RuntimeException(String.format("The METADATA.json file in %s could not be read",
          path), e);
    }
    return gson.fromJson(json, FamilyMetadata.class);
  }
}
