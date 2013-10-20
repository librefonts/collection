package com.google.lint.common;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;

import java.util.List;
import java.util.Map;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class Context {

  private final Map<Severity, List<String>> reports = Maps.newHashMap(); 

  public void report(Severity severity, String report) {
    List<String> severityReports = reports.get(severity);
    if (severityReports == null) {
      severityReports = Lists.newArrayList();
      reports.put(severity, severityReports);
    }
    severityReports.add(report);
  }

  public void printReports() {

    // The enum is ordered from highest severity to lowest
    for (Severity severity : Severity.values()) {
      List<String> severityReports = reports.get(severity);
      if (severityReports != null) {
        for (String report : severityReports) {
          System.out.println(String.format("[%s] %s", severity, report));
        } 
      }
    }
  }
}
