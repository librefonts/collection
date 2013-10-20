// Copyright 2012 Google. All Rights Reserved.
package com.google.lint;

import com.google.common.collect.Lists;
import com.google.inject.Guice;
import com.google.inject.Inject;
import com.google.inject.Injector;
import com.google.lint.common.Context;
import com.google.lint.common.LintCheck;

import java.util.List;
import java.util.Set;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class Lint {

  private final Context context;
  private final Set<LintCheck> lintChecks;

  @Inject
  public Lint(Context context, Set<LintCheck> lintChecks) {
    this.context = context;
    this.lintChecks = lintChecks;
  }

  public void run(List<String> familyDirectories) {
    for (LintCheck lintCheck : lintChecks) {
      lintCheck.run(context, familyDirectories);
    }
    context.printReports();
  }

  public static void main(String[] args) {
    Injector injector = Guice.createInjector(new LintModule());
    Lint lint = injector.getInstance(Lint.class);

    try {
      lint.run(Lists.newArrayList(args));
    } catch (Throwable cause) {
      cause.printStackTrace();
      System.exit(1);
    }
    System.exit(0);
  }
}
