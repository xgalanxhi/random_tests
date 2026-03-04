# JUnit XML Validator for Smart Tests

Pre-flight validation tool for JUnit XML test reports before sending to CloudBees Smart Tests.

## Quick Start

```bash
# Validate all XML files in a directory
python3 tools/validate_junit_xml.py cicd/temp/test-results/

# Validate a single file
python3 tools/validate_junit_xml.py test-results/junit.xml

# Mix files and directories
python3 tools/validate_junit_xml.py report1.xml report2.xml results/
```

## What It Checks

### Critical Issues (Errors)

These will **block Smart Tests** from processing your reports correctly:

| Issue | Why It Matters |
|-------|----------------|
| **Missing `classname` attribute** | Smart Tests uses `classname` to map tests to source files. Without it, Predictive Test Selection cannot correlate code changes to affected tests. |
| **Missing `name` attribute** | Every test case must have a unique identifier. Smart Tests cannot track results without names. |
| **Invalid XML** | Malformed XML (unclosed tags, encoding issues) cannot be parsed. |
| **Wrong root element** | JUnit XML must start with `<testsuites>` or `<testsuite>`. |

### Warnings

These reduce Smart Tests effectiveness but won't block ingestion:

| Issue | Impact |
|-------|--------|
| **Missing `time` attribute** | Smart Tests cannot estimate subset execution time. Time-based targets (e.g., `--target 50%`) will be inaccurate. |
| **No test suite names** | Reduces dashboard organization and filtering capabilities. |
| **Empty test suites** | Provides no data to Smart Tests. |

### Informational

Best practices for optimal Smart Tests features:

| Recommendation | Benefit |
|----------------|---------|
| **Include `<system-out>` / `<system-err>`** | AI triage features work best with stdout/stderr. Enables automatic failure analysis and root cause suggestions. |
| **Include some failures in history** | Smart Tests learns which tests catch which bugs by seeing failure patterns. Provide at least 6 runs spanning 1-2 weeks that include some failures. |

## When to Use This Tool

### 1. Sales Engineering Prep

Before a Smart Tests demo:

```bash
# Validate customer's existing test reports
python3 tools/validate_junit_xml.py /path/to/customer/test-results/

# Check for blockers
```

Common findings and fixes:

- **Maven Surefire missing classname**: Add `<testSourceDirectory>` to pom.xml
- **pytest missing classname**: Outdated pytest or plugin issue — update to pytest ≥7.x
- **Custom test runners**: May need to switch to `file` or `raw` format with explicit path mapping

### 2. Customer Self-Service

Share this tool with customers during onboarding:

```bash
# Before first smart-tests record tests
python3 validate_junit_xml.py build-123/test-results/

# Fix errors, then:
smart-tests record tests pytest build-123/test-results/
```

### 3. CI Integration

Add validation as a pre-flight check:

```yaml
# GitHub Actions
- name: Validate test reports
  run: python3 tools/validate_junit_xml.py test-results/
  if: always()  # Run even if tests failed

- name: Send to Smart Tests
  run: smart-tests record tests pytest test-results/
  if: always()
```

```groovy
// Jenkins
stage('Validate Reports') {
    steps {
        sh 'python3 tools/validate_junit_xml.py test-results/'
    }
}
stage('Report to Smart Tests') {
    steps {
        sh 'smart-tests record tests pytest test-results/'
    }
}
```

### 4. Troubleshooting

When `smart-tests record tests` fails or shows unexpected results:

```bash
# Run validator to identify issues
python3 tools/validate_junit_xml.py cicd/temp/test-results/

# Common symptoms:
# - "0 tests recorded" → missing <testcase> elements
# - "Cannot map tests to files" → missing classname attributes
# - "Estimated duration is 0.00" → missing time attributes
```

## Common Issues by Framework

### pytest

**Missing `classname`**: Update to pytest ≥7.0. Older versions may not include classname in JUnit XML.

```bash
pip install --upgrade pytest
pytest --junit-xml=results.xml
```

**Missing `time`**: pytest includes test duration by default. If missing, check for custom JUnit XML plugins that override default behavior.

**Fix**: Use default pytest JUnit XML generation or ensure custom plugins preserve `time` attributes.

### Maven Surefire

**Missing `classname`**: Configure `<testSourceDirectory>` in pom.xml:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <configuration>
    <testSourceDirectory>src/test/java</testSourceDirectory>
  </configuration>
</plugin>
```

**System output not captured**: Surefire captures stdout/stderr by default. If missing, check for redirected output or custom test runners.

### Jest

**Missing `classname`**: Configure jest-junit reporter with `classNameTemplate`:

```json
{
  "reporters": [
    "default",
    ["jest-junit", {
      "outputDirectory": "./test-results",
      "outputName": "junit.xml",
      "classNameTemplate": "{filepath}"
    }]
  ]
}
```

**Missing `time`**: jest-junit includes duration by default. Ensure reporter version ≥13.0.

### Gradle

**Missing `classname`**: Gradle's default JUnit XML includes classname. If missing, check for custom test tasks or plugins overriding XML generation.

**Fix**: Use default Gradle test task XML output from `build/test-results/test/`.

### Custom / Other Frameworks

If your framework generates non-standard JUnit XML:

1. **Option A**: Use Smart Tests `file` or `raw` format with explicit path mapping
2. **Option B**: Post-process XML to add missing attributes:

```python
import xml.etree.ElementTree as ET

tree = ET.parse("results.xml")
for testcase in tree.findall(".//testcase"):
    if not testcase.get("classname"):
        # Derive classname from file path
        testcase.set("classname", "my.package.TestClass")
tree.write("results-fixed.xml")
```

## JUnit XML Format Reference

Smart Tests expects JUnit XML as defined by [testmoapp/junitxml](https://github.com/testmoapp/junitxml):

### Minimal Valid Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="MyTestSuite" tests="2" failures="0" errors="0" time="1.234">
    <testcase name="test_addition" classname="test.test_math" time="0.001">
      <system-out>Test output here</system-out>
    </testcase>
    <testcase name="test_subtraction" classname="test.test_math" time="0.002">
      <system-out>More output</system-out>
    </testcase>
  </testsuite>
</testsuites>
```

### Required Attributes

| Element | Attribute | Required | Purpose |
|---------|-----------|----------|---------|
| `<testcase>` | `name` | Yes | Unique test identifier |
| `<testcase>` | `classname` | **Yes** | Maps test to source file (PTS requirement) |
| `<testcase>` | `time` | Recommended | Test duration in seconds (for subset time estimates) |
| `<testsuite>` | `name` | Recommended | Suite identifier for dashboard organization |

### Outcome Elements

Add inside `<testcase>` to indicate non-passing results:

- `<failure>`: Test assertion failed
- `<error>`: Test threw an exception
- `<skipped>`: Test was skipped

Passing tests have no outcome element.

### Output Capture

Add inside `<testcase>` or `<testsuite>`:

- `<system-out>`: Captured stdout
- `<system-err>`: Captured stderr

**Why it matters**: Smart Tests AI triage features analyze output to suggest root causes for failures.

## Exit Codes

- `0`: All files valid
- `1`: One or more files have errors
- `2`: Invalid usage (no files provided)

Use in CI to fail the build if XML is invalid:

```bash
python3 tools/validate_junit_xml.py test-results/ || exit 1
```

## See Also

- [Smart Tests Integrations](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/integrations/)
- [JUnit XML Format Spec](https://github.com/testmoapp/junitxml)
- [Smart Tests Onboarding Guide](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/resources/onboarding-guide)
