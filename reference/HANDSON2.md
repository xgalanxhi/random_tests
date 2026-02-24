# Lab 2. Try predictive test selection

In this section, you will test drive Predictive Test Selection (PTS) on your own computer.
Along the way, you will learn the major concepts of Smart Test.

## Clone your repository
To experiment with Smart Tests, first, let's clone your repository locally.
How to do this depends on your project.

If you already cloned repository, please skip cloning the repository and move to the repo directory.

```
git clone ...
cd your/repository
```

## Capture software under test

In order to select the right tests for your software, Smart Tests need to know what software you are testing. We call this a **build**.

A build is a specific version of your software that you are testing. It can consist of multiple Git repositories, and in each repository, it points to a specific commit. A build is identified by its name.

> **build** represents the software. Each time you send test results to Smart Test, you record them against a specific build so that Smart Tests know that you ran X tests against Y software with Z results.

refs: [Documentation](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/concepts/build)

Therefore, before you run your tests, you record a build using `smart-tests record build`.

Move to the locally checked out copy of your software, check out its main branch,
and run the following command to record a build:
```
smart-tests record build --build baseline
```
If you see a message like this, it was successful:

```
Launchable recorded 2 more commits from repository <YOUR PATH>
Launchable recorded build hands-on to workspace <YOUR ORG/WORKSPACE> with commits from 1 repository:

| Name   | Path   | HEAD Commit                              |
|--------|--------|------------------------------------------|
| .      | .      | 3f21bfb3d56148c9dcf9f7e811e146bbc3cbf797 |

Visit https://app.launchableinc.com/organizations/<ORG>/workspaces/<WORKSPACE>/data/builds/<BUILD ID> to view this build and its test sessions
```

What just happened? Smart Tests recorded the current HEAD of your local repository as the build,
using the name given.

>[!NOTE]
> If you have multiple repositories, please check [this document](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/sending-data-to-smart-tests/recording-builds/recording-builds-from-multiple-repositories) to let Smart Tests know that the build consists of your repositories.


Since this was the first time you recorded a build, Smart Tests needed to transfer relatively
large amount of data to its server, including recent commit history, file contents, etc. It
also has to do a lot of number crunching to prepare for the predictive test selection.

But subsequent calls to `smart-tests record build` will be much faster, because Smart Tests will only transfer the new commits that you have added since the last build.

## Request and inspect a subset to test
Now, you declare the start of a new test session; A test session is an act of running tests against a specific build. Test selection and recording of test results are done against a test session.

 refs: [Documentation](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/concepts/test-session)

 ```
 smart-tests record session --build baseline --test-suite my-test-suite > session.txt
 ```

When you record a new test session, Smart Tests will return a session ID, which is stored in `session.txt` file.

Now, let's have Smart Tests create a subset of the tests... except, we don't know the right size of the subset to create, so instead we'll select all the tests. Smart Tests still produce tests in the relevance order, so this way we can see how tests are ranked:

```
smart-tests subset file --session @session.txt --get-tests-from-guess > subset.txt
```

Let's see what's inside:
```
less subset.txt
```

Since you haven't run any tests yet, Smart Tests will select files in your repository
that looks like tests (`--get-tests-from-guess`).

The output will look like this:

```
Smart Tests created subset <SUBSET_ID> for build baseline (test session <TEST_SESSION_ID>) in workspace <ORG>/<WORKSPACE>

|           |   Candidates |   Estimated duration (%) |   Estimated duration (min) |
|-----------|--------------|--------------------------|----------------------------|
| Subset    |          120 |                   100.00 |                       0.00 |
| Remainder |            0 |                     0.00 |                       0.00 |
|           |              |                          |                            |
| Total     |          120 |                   100.00 |                       0.00 |

Run `smart-tests inspect subset --subset-id <SUBSET_ID>` to view full subset details
```

> [!TIP]
> Note the **subset ID** (e.g., `<SUBSET_ID>` in the example above). We'll use this ID later to compare
> how additional changes affect the test selection, so please keep it noted.


As you run and record test results, Smart Tests will learn from the results and improve its selection.
Among other things, you will be able to specify the size of the subset you'd like to obtain, for example
"give me 10 minutes worth of tests to run".



## Make a change you want to test, and see how that affects the subset
When a developer makes a change to the code, we want Smart Tests to select the tests that
are most relevant to that change. To experiment with this, let's make a small change.
Don't worry, the commit you'll create will stay in your computer.

```
vim <UPDATE YOUR APP or TEST CODE>
git commit --all --message test
```

We now have a new software version to test, so we need to record it as a new build:

```
smart-tests record build --build mychange
```

Create a new test session against the new build:

```
smart-tests record session --build mychange --test-suite my-test-suite > session2.txt
```

Now, let's have Smart Tests sort the tests by their relevance to your change (`--use-case one-commit`):

```
smart-tests subset file --session @session2.txt --use-case one-commit --get-tests-from-guess > subset2.txt
```

Compare the results between the first and the second subsets. First, get the subset IDs from the output of the subset commands, then run:

```
smart-tests compare subsets --subset-id-before <SUBSET_ID_1> --subset-id-after <SUBSET_ID_2>
```

The command should display the rank of every test in those two subsets, and highlight the differences in the rank.
You should see that the tests relevant to your change bubble up in the rank.


You can now move on to [the next step](HANDSON3.md).
