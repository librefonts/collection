package com.google.lint.common;

import java.util.List;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public interface LintCheck {

  void run(Context context, List<String> familyDirectories);
}
