# Migration from Launchable to Smart Tests CLI

## Changes Made

All references to Launchable have been replaced with Smart Tests CLI throughout the project.

### 1. Dependencies (`requirements.txt`)
```diff
- launchable~=1.120.0
+ smart-tests-cli~=2.0
```

### 2. Commands Updated

All `launchable` commands replaced with `smart-tests`:
- `launchable record build` → `smart-tests record build`
- `launchable record session` → `smart-tests record session`
- `launchable subset` → `smart-tests subset`
- `launchable record tests` → `smart-tests record tests`

### 3. File Names Simplified

Temporary files renamed for simplicity:
- `launchable-session.txt` → `session.txt`
- `launchable-subset.txt` → `subset.txt`

### 4. Files Updated

#### Code & Config:
- ✅ `requirements.txt` - Updated to smart-tests-cli~=2.0
- ✅ `cicd/pipeline.sh` - All commands and file names updated
- ✅ `.cloudbees/workflows/pipeline.yaml` - Container and environment variables updated

#### Documentation:
- ✅ `CLAUDE.md` - All references updated
- ✅ `README.md` - All references, URLs, and examples updated

### 5. Environment Variables

- `LAUNCHABLE_TOKEN` → `SMART_TESTS_TOKEN`
- CloudBees secret remains: `SMART_TESTS_KEY`

### 6. Docker Container

CloudBees workflow now uses:
```yaml
uses: docker://cloudbees/smart-tests-cli:v2.0
```

### 7. URLs Updated

- `app.launchableinc.com` → `app.cloudbees.com/smart-tests`
- `docs.launchableinc.com` → `docs.cloudbees.com/docs/cloudbees-smart-tests`
- `launchableinc.com/community` → `cloudbees.com/community`

## Usage

### Installation
```bash
pip install -r requirements.txt
```

### Environment Setup
```bash
export SMART_TESTS_TOKEN="<your-token>"
```

### Verify Installation
```bash
smart-tests --version
# Should show: smart-tests, version 2.0
```

### Run Pipeline
```bash
./cicd/pipeline.sh 5
```

### Check Generated Files
```bash
ls cicd/temp/
# session.txt
# subset.txt
# test-results/
```

## Benefits

1. **Simplified naming** - Shorter file names (session.txt, subset.txt)
2. **Updated CLI** - Using latest Smart Tests CLI 2.0
3. **Consistent branding** - CloudBees Smart Tests throughout
4. **Better documentation** - Links to CloudBees documentation
