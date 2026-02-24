# Lab 3. Incorporate Smart Tests into your CI workflow

In this section, you will use a toy Java project in this repository and its delivery workflow based on GitHub Action as an example, to gain better understanding of how to use Smart Tests in your CI workflow.

# Before you start
Your instructor should have created a pull request to `cloudbees-oss/smart-tests-hands-on-lab`. This is where the toy Java
project resides, and in this PR we'll modify its CI pipeline.

# Integrating with Smart Tests

Start with the PR, and follow the "edit CI script" link in the PR description to open the CI script in the editor.

<img width="742" height="425" alt="image" src="https://github.com/user-attachments/assets/b4e5749a-a226-4607-af50-58d96d879848" />

## Add the Smart Tests CLI to workflow
Update `.github/workflows/pre-merge.yml` as follows:

```diff
        with:
          java-version: 21
          distribution: "adopt"
+     - uses: actions/setup-python@v5
+       with:
+         python-version: '3.13'
+     - name: Install Smart Tests CLI
+       run: pip install --user --upgrade smart-tests-cli~=2.0
      - name: Compile
        run: mvn compile
```
<details>
<summary>Raw text for copying</summary>

```
- uses: actions/setup-python@v5
  with:
    python-version: '3.13'
- name: Install Smart Tests CLI
  run: pip install --user --upgrade smart-tests-cli~=2.0
```

</details>
<br>

## Verify the Smart Tests CLI setup
Next, to help you make sure that you have everything set up correctly, we have the `smart-tests verify` command, so we'll add it to the workflow as well.

Update `.github/workflows/pre-merge.yml` as follows:
```diff
       - name: Install Smart Tests CLI
         run: pip install --user --upgrade smart-tests-cli~=2.0
+      - name: Smart Tests verify
+        run: smart-tests verify
       - name: Compile
         run: mvn compile
       - name: Test
```

<details>
<summary>Raw texts for copying</summary>

```
- name: Smart Tests verify
  run: smart-tests verify
```

</details>
<br>

## Commit the changes
Add these changes to the PR by clicking on **Commit changes**.

<img width="407" height="151" alt="image" src="https://github.com/user-attachments/assets/7687ca9e-2c30-4c2b-bf0c-c093d65c7f21" />

(Commit directly to the branch, as opposed to create a new branch)

When the commit goes through, come back to the PR page to see the newly added commit. Depending on the status of the CI run, you will see one of the icons on the left of the commit hash:

<img width="672" height="83" alt="image" src="https://github.com/user-attachments/assets/afb51dd1-353f-4b6d-b453-e47c37f7184e" />

* 🟡 if a CI run is ongoing
* ❌ if a CI run has failed
* ✔️ if a CI run has completed successfully
* None if a CI run hasn't started, or if there was a syntax error in the edit you just made.

> [!TIP]
> You might have to reload the page to see the commit and its status updated.

Using the following screenshot as an example, click the status symbol, and select "details" to jump to the CI log.

<img width="723" height="169" alt="image" src="https://github.com/user-attachments/assets/997dd7ef-87a7-4d8d-b917-b37d5b46895a" />

If everything goes as expected, in the "Smart Tests verify" section, you should see a message like this:

```
Organization: launchable-demo
Workspace: hands-on-lab
Proxy: None
Platform: 'Linux-6.8.0-1017-azure-x86_64-with-glibc2.39'
Python version: '3.13.0'
Java command: 'java'
smart-tests version: '2.2.0'
Your CLI configuration is successfully verified 🎉
```

# Recording build information
Now, let's record the build information. We've already looked at what this does in Lab 2.

## Enable full Git history

Update `.github/workflows/pre-merge.yml` as follows:
```diff
steps:
       - uses: actions/checkout@v5
+        with:
+          fetch-depth: 0
       - uses: actions/setup-java@v4
         with:
           java-version: 11
```

<details>
<summary>Raw text for copying</summary>

```
with:
  fetch-depth: 0
```

</details>
<br>

## Record build with Smart Tests CLI
Next, execute the `smart-tests record build` command.

Update `.github/workflows/pre-merge.yml` as follows:
```diff
run: pip install --user --upgrade smart-tests-cli~=2.0
       - name: Smart Tests verify
         run: smart-tests verify
+      - name: Smart Tests record build
+        run: smart-tests record build --build ${{ github.run_id }}
       - name: Compile
         run: mvn compile
   worker-node-1:
```

<details>
<summary>Raw text for copying</summary>

```
- name: Smart Tests record build
  run: smart-tests record build --build ${{ github.run_id }}
```

</details>
<br>

Commit changes directly to your branch by clicking on **Commit changes**. If the setup is successful, you will see logs similar to the following:

```
Launchable recorded 1 commit from repository /home/runner/work/hands-on/hands-on
Launchable recorded build 3096604891 to workspace organization/workspace with commits from 1 repository:
| Name   | Path   | HEAD Commit                              |
|--------|--------|------------------------------------------|
| .      | .      | 5ea0a739271071dfbdacd330b0cc28c307151a04 |
```

# Running test session by predicting a subset
Now, we will start a test session. We have also looked at this in Lab 2.

## Add Smart Tests subset command
We will first obtain the subset of tests that should be run for this build. then pass it to the test runner, which is Maven in this case.

Notice the `--observation` flag. This is [the training wheel mode](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/features/predictive-test-selection/observing-subset-behavior). With this flag, Smart Test
will go through all the motions, except for actually returning all the tests. We'll use this mode
to observe the behavior/performance of the test selection, hence the name.

Update `.github/workflows/pre-merge.yml` as follows:
```diff
      - name: Compile
        run: mvn compile
+     - name: Smart Tests subset
+       run: |
+         smart-tests record session --build ${{ github.run_id }} --observation --test-suite unit-test > session.txt
+         smart-tests subset maven --session @session.txt --target 50% src/test/java > smart-tests-subset.txt
+         cat smart-tests-subset.txt
      - name: Test
        run: mvn test
```
<details>
<summary>Raw text for copying</summary>

```
- name: Smart Tests subset
  run: |
    smart-tests record session --build ${{ github.run_id }} --observation --test-suite unit-test > session.txt
    smart-tests subset maven --session @session.txt --target 50% src/test/java > smart-tests-subset.txt
    cat smart-tests-subset.txt
```

</details>
<br>

Commit changes directly to your branch by clicking on **Commit changes**. If the setup is successful, you will see logs similar to the following, although the details might vary:

```
|           |   Candidates |   Estimated duration (%) |   Estimated duration (min) |
|-----------|--------------|--------------------------|----------------------------|
| Subset    |            2 |                  36.4706 |                  0.0516667 |
| Remainder |            2 |                  63.5294 |                  0.09      |
|           |              |                          |                            |
| Total     |            4 |                 100      |                  0.141667  |
Run `launchable inspect subset --subset-id XXX` to view full subset details
example.MulTest
example.DivTest
example.AddTest
example.SubTest
```

## Run Maven tests with subset
Next, pass this subset to the test runner.

```diff

      - name: Test
-       run: mvn test
+       run: mvn test -Dsurefire.includesFile=smart-tests-subset.txt
```
<details>
<summary>Raw text for copying</summary>

```
run: mvn test -Dsurefire.includesFile=smart-tests-subset.txt
```

</details>
<br>

Commit changes directly to your branch by clicking on **Commit changes**.

# Record test results
After tests are run, you need to report the test results to Smart Tests. This is done by the **smart-tests record tests** command.

If the test fail, GitHub Actions will stop the job and the test results will not be reported to Smart Tests. Therefore, you need to set `if: always()` so that test results are always reported.

## Record tests to Smart Tests

Update `.github/workflows/pre-merge.yml` as follows:
```diff
      - name: Test
        run: mvn test -Dsurefire.includesFile=smart-tests-subset.txt
+     - name: Smart Tests record tests
+       if: always()
+       run: smart-tests record tests maven --session @session.txt ./**/target/surefire-reports
```
<details>
<summary>Raw text for copying</summary>

```
- name: Smart Tests record tests
  if: always()
  run: smart-tests record tests maven --session @session.txt ./**/target/surefire-reports
```

</details>
<br>

Commit changes directly to your branch by clicking on **Commit changes**.

# Check results in Launchable web-app
If everything is set up correctly, you can view the test results on Launchable as shown below: (A URL to this page is in the GitHub Actions log)

<img src="https://github.com/user-attachments/assets/f83dd1e6-bf9e-4091-964c-da665ffd764d" width="50%">

You should also see the report from the subset observation:

![image](https://user-images.githubusercontent.com/536667/195477376-500d318a-b67a-4202-8c90-81ca6048dcc4.png)

# Go live
If this was a real project, we'd keep the `--observation` flag until we accumulate enough data, then
evaluate its performance & roll out. In this workshop, we can skip this step and go live right away.

```diff
      - name: Smart Tests subset
        run: |
-        smart-tests record session --build ${{ github.run_id }} --observation --test-suite unit-test > session.txt
+        smart-tests record session --build ${{ github.run_id }} --test-suite unit-test > session.txt
         smart-tests subset maven --session @session.txt --target 50% src/test/java > smart-tests-subset.txt
      - name: Test
        run: mvn test
```

Let's apply this change and check the result.

Commit changes directly to your branch by clicking on **Commit changes**.
