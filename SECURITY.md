# Security Policy

## Supported versions

Only the latest release of pyml-datasets gets security fixes.

## Reporting a vulnerability

Please do **not** open a public issue for a security problem.

Use the private reporting of GitHub: open the **Security and quality** tab of this repository
and choose **Report a vulnerability**. Describe what you found, the version it affects and, if
you can, how to reproduce it.

This is a personal project run by one maintainer, so I may be slow, but I will read every
report and answer it as soon as I can.

## What is and is not a security issue

The data files are read with NumPy's `allow_pickle=False`, so loading a dataset never runs
code from the file. A report is welcome if a data file, its hash or the build and release
process can be used to put wrong or harmful content in front of users.

Like NumPy, this library is not meant to be exposed directly to untrusted users: somebody who
can already run Python code in your process does not need a vulnerability here. Report such
cases as regular bugs.
