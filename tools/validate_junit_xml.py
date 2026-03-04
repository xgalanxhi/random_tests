#!/usr/bin/env python3
"""
Validate JUnit XML files for CloudBees Smart Tests compatibility.

Checks that XML files conform to the JUnit XML format expected by the
Smart Tests CLI (smart-tests record tests). Run this against your test
reports before sending them to Smart Tests to catch formatting issues early.

Usage:
    python validate_junit_xml.py path/to/results/          # validate all XML in directory
    python validate_junit_xml.py report.xml                 # validate single file
    python validate_junit_xml.py a.xml b.xml results/       # mix of files and dirs

Reference: https://github.com/testmoapp/junitxml
"""

import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Message types
# ---------------------------------------------------------------------------

@dataclass
class Issue:
    level: str          # ERROR, WARN, INFO
    file: str
    location: str       # e.g. "testsuite[0]/testcase[2]"
    message: str


@dataclass
class ValidationResult:
    file: str
    issues: list = field(default_factory=list)
    test_count: int = 0
    suite_count: int = 0
    has_failures: bool = False
    has_durations: bool = False
    has_output: bool = False

    @property
    def errors(self):
        return [i for i in self.issues if i.level == "ERROR"]

    @property
    def warnings(self):
        return [i for i in self.issues if i.level == "WARN"]

    @property
    def passed(self):
        return len(self.errors) == 0


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def validate_file(filepath: str) -> ValidationResult:
    """Validate a single JUnit XML file for Smart Tests compatibility."""
    result = ValidationResult(file=filepath)

    # --- Can we parse it at all? ---
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        result.issues.append(Issue(
            "ERROR", filepath, "document",
            f"Invalid XML: {e}\n"
            f"  → The file must be well-formed XML. Check for unclosed tags,\n"
            f"    invalid characters, or encoding issues."
        ))
        return result
    except Exception as e:
        result.issues.append(Issue(
            "ERROR", filepath, "document",
            f"Cannot read file: {e}"
        ))
        return result

    root = tree.getroot()

    # --- Root element ---
    # Strip namespace if present (some frameworks add xmlns)
    root_tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag

    if root_tag == "testsuites":
        suites = root.findall("testsuite")
        if not suites:
            # Some frameworks nest: testsuites > testsuite > testsuite
            suites = root.findall(".//testsuite")
        if not suites:
            result.issues.append(Issue(
                "ERROR", filepath, "testsuites",
                "Root <testsuites> contains no <testsuite> elements.\n"
                "  → Each <testsuites> must contain at least one <testsuite>."
            ))
            return result

    elif root_tag == "testsuite":
        # Single testsuite as root is valid
        suites = [root]

    else:
        result.issues.append(Issue(
            "ERROR", filepath, "document",
            f"Root element is <{root.tag}>, expected <testsuites> or <testsuite>.\n"
            f"  → JUnit XML must have <testsuites> or <testsuite> as the root element.\n"
            f"  → See: https://github.com/testmoapp/junitxml"
        ))
        return result

    result.suite_count = len(suites)

    # --- Validate each testsuite ---
    for si, suite in enumerate(suites):
        suite_loc = f"testsuite[{si}]"
        suite_name = suite.get("name", "(unnamed)")

        # Suite name attribute
        if not suite.get("name"):
            result.issues.append(Issue(
                "WARN", filepath, suite_loc,
                "Missing 'name' attribute on <testsuite>.\n"
                "  → Smart Tests uses suite names for organization in the dashboard."
            ))

        # --- Validate test cases ---
        testcases = suite.findall("testcase")
        if not testcases:
            result.issues.append(Issue(
                "WARN", filepath, suite_loc,
                f"<testsuite name=\"{suite_name}\"> contains no <testcase> elements.\n"
                "  → Empty suites provide no data to Smart Tests."
            ))
            continue

        for ti, tc in enumerate(testcases):
            tc_loc = f"{suite_loc}/testcase[{ti}]"
            tc_name = tc.get("name", "(unnamed)")
            result.test_count += 1

            # --- Required: name ---
            if not tc.get("name"):
                result.issues.append(Issue(
                    "ERROR", filepath, tc_loc,
                    "Missing 'name' attribute on <testcase>.\n"
                    "  → Every <testcase> must have a 'name'. This is how Smart Tests\n"
                    "    identifies individual tests."
                ))

            # --- Required: classname ---
            if not tc.get("classname"):
                result.issues.append(Issue(
                    "ERROR", filepath, tc_loc,
                    f"Missing 'classname' attribute on <testcase name=\"{tc_name}\">.\n"
                    "  → Smart Tests uses 'classname' to map tests back to source files.\n"
                    "    Without it, Predictive Test Selection cannot correlate code\n"
                    "    changes to affected tests.\n"
                    "  → Example: <testcase name=\"test_add\" classname=\"test.test_calculator\">"
                ))

            # --- Recommended: time ---
            time_val = tc.get("time")
            if time_val is not None:
                result.has_durations = True
                try:
                    t = float(time_val)
                    if t < 0:
                        result.issues.append(Issue(
                            "WARN", filepath, tc_loc,
                            f"Negative time value ({time_val}) on <testcase name=\"{tc_name}\">."
                        ))
                except ValueError:
                    result.issues.append(Issue(
                        "WARN", filepath, tc_loc,
                        f"Non-numeric time value '{time_val}' on <testcase name=\"{tc_name}\">.\n"
                        "  → The 'time' attribute should be seconds as a decimal number."
                    ))
            else:
                result.issues.append(Issue(
                    "WARN", filepath, tc_loc,
                    f"Missing 'time' attribute on <testcase name=\"{tc_name}\">.\n"
                    "  → Smart Tests uses test duration to estimate subset execution time.\n"
                    "    Without it, time-based targets (e.g. --target 50%) will be\n"
                    "    inaccurate and estimated durations will show 0.00."
                ))

            # --- Check outcome: must be binary pass/fail ---
            failure = tc.find("failure")
            error = tc.find("error")
            skipped = tc.find("skipped")

            if failure is not None:
                result.has_failures = True
            if error is not None:
                result.has_failures = True

            # --- Recommended: system-out / system-err ---
            sys_out = tc.find("system-out")
            sys_err = tc.find("system-err")
            if sys_out is not None or sys_err is not None:
                result.has_output = True

    # --- Suite-level checks also count for output ---
    for suite in suites:
        if suite.find("system-out") is not None or suite.find("system-err") is not None:
            result.has_output = True

    # --- Aggregate warnings ---
    if not result.has_durations and result.test_count > 0:
        result.issues.append(Issue(
            "WARN", filepath, "summary",
            "No test cases have 'time' attributes.\n"
            "  → Smart Tests will not be able to estimate subset execution time.\n"
            "    Time-based subset targets will be inaccurate."
        ))

    if not result.has_output and result.test_count > 0:
        result.issues.append(Issue(
            "INFO", filepath, "summary",
            "No <system-out> or <system-err> elements found.\n"
            "  → Smart Tests AI triage features work best when stdout/stderr are\n"
            "    captured in test reports. Most test frameworks support this:\n"
            "    - pytest: use --capture=sys or default capture\n"
            "    - Maven Surefire: captured by default\n"
            "    - Jest: use --verbose"
        ))

    if not result.has_failures and result.test_count > 0:
        result.issues.append(Issue(
            "INFO", filepath, "summary",
            "All tests passed (no failures or errors found).\n"
            "  → This is fine for a single report, but Smart Tests needs to see\n"
            "    some failures across your history to learn which tests catch\n"
            "    which kinds of bugs. Provide at least 6 runs spanning 1-2 weeks\n"
            "    that include some failures."
        ))

    return result


# ---------------------------------------------------------------------------
# Collect files
# ---------------------------------------------------------------------------

def collect_xml_files(paths: list) -> list:
    """Resolve a mix of files and directories into XML file paths."""
    xml_files = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            if path.suffix.lower() == ".xml":
                xml_files.append(str(path))
            else:
                print(f"  Skipping non-XML file: {path}")
        elif path.is_dir():
            found = sorted(path.rglob("*.xml"))
            if not found:
                print(f"  No XML files found in: {path}")
            xml_files.extend(str(f) for f in found)
        else:
            print(f"  Path not found: {path}")
    return xml_files


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

SYMBOLS = {"ERROR": "✗", "WARN": "⚠", "INFO": "ℹ"}
COLORS = {
    "ERROR": "\033[91m",    # red
    "WARN":  "\033[93m",    # yellow
    "INFO":  "\033[90m",    # gray
    "RESET": "\033[0m",
    "BOLD":  "\033[1m",
    "GREEN": "\033[92m",
}

def use_color():
    """Check if stdout supports color."""
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def print_result(result: ValidationResult, color: bool = True):
    c = COLORS if color else {k: "" for k in COLORS}

    # Header
    status = f"{c['GREEN']}✓ PASS{c['RESET']}" if result.passed else f"{c['ERROR']}✗ FAIL{c['RESET']}"
    print(f"\n{c['BOLD']}{result.file}{c['RESET']}  {status}")
    print(f"  {result.suite_count} suite(s), {result.test_count} test case(s)")

    if not result.issues:
        print(f"  {c['GREEN']}No issues found.{c['RESET']}")
        return

    # Group by level
    for level in ["ERROR", "WARN", "INFO"]:
        level_issues = [i for i in result.issues if i.level == level]
        if not level_issues:
            continue
        for issue in level_issues:
            sym = SYMBOLS[level]
            clr = c[level]
            # Indent continuation lines
            lines = issue.message.split("\n")
            first = lines[0]
            rest = "\n".join(f"      {l}" for l in lines[1:])
            print(f"  {clr}{sym} [{issue.location}] {first}{c['RESET']}")
            if rest.strip():
                print(f"{c[level]}{rest}{c['RESET']}")


def print_summary(results: list, color: bool = True):
    c = COLORS if color else {k: "" for k in COLORS}

    total_files = len(results)
    passed_files = sum(1 for r in results if r.passed)
    failed_files = total_files - passed_files
    total_tests = sum(r.test_count for r in results)
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)

    print(f"\n{'─' * 60}")
    print(f"{c['BOLD']}Smart Tests XML Validation Summary{c['RESET']}")
    print(f"{'─' * 60}")
    print(f"  Files validated:  {total_files}")
    print(f"  Total test cases: {total_tests}")

    if failed_files:
        print(f"  {c['ERROR']}Files with errors: {failed_files}{c['RESET']}")
    if total_errors:
        print(f"  {c['ERROR']}Errors:            {total_errors}{c['RESET']}")
    if total_warnings:
        print(f"  {c['WARN']}Warnings:          {total_warnings}{c['RESET']}")

    if failed_files == 0:
        print(f"\n  {c['GREEN']}All files are compatible with Smart Tests.{c['RESET']}")
    else:
        print(f"\n  {c['ERROR']}Fix errors above before running: smart-tests record tests{c['RESET']}")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Error: provide one or more XML files or directories to validate.")
        sys.exit(2)

    paths = sys.argv[1:]
    xml_files = collect_xml_files(paths)

    if not xml_files:
        print("No XML files found to validate.")
        sys.exit(2)

    color = use_color()
    results = []

    for f in xml_files:
        result = validate_file(f)
        results.append(result)
        print_result(result, color)

    print_summary(results, color)

    # Exit code: 1 if any errors, 0 otherwise
    has_errors = any(not r.passed for r in results)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
