# Lab 0. Prerequisites 

The following are prerequisites for this workshop:

1. Look into your internal infosec policies and make sure you can let CloudBees process your source code during this workshop. Note we do not store your source code, nor are they used to train any AI models. See [data privacy and protection policy](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/resources/policies/data-privacy-and-protection) for more details.

1. Provide recent test results data from your actual project in the standardized JUnit XML format described [here](https://github.com/testmoapp/junitxml). This allows us to personalize your workshop experience by pre-populating Smart Tests dashboards and highlighting insights such as _Unhealthy tests_, _Trends_ and _AI-based failure triage_.
   - Provide **atleast 6 recent runs** worth of test results (ideally spanning 1–2 weeks)
   - Include runs with both **passing and failing tests**
   - Make sure `stdout` and `stderr` logs are captured in your reports
   - If your XML files are in a different format, please contact us.

1. You need a computer with `git`, `python3` (3.13 or later), and `java` installed.

1. Prepare a repository that contains test code where you want to try PTS. We recommend using a repository you normally work with. (You will not need to push any code during the hands-on.)

1. Share your GitHub ID with us, so that we can add you as a collaborator to the workshop.

1. Follow the invitation link we send to you, and perform the sign-up process.

## Install Smart Tests command

You interact with Smart Tests using a command line tool called `smart-tests`.

You can install it with [uv](https://docs.astral.sh/uv/):

```
uv tool install smart-tests-cli~=2.0
```

Let's check that it's installed correctly:

```
smart-tests --help
```

>[!TIP]
> If `smart-tests` is not found on your `PATH`
> <details>
> Run the following command to find out where `pip3` installed the script:
>
> ```
> pip3 show --files smart-tests-cli | grep -E 'bin/smart-tests$|^Location'
> ```
>
> This command will produce output like this:
>
> ```
> Location: /home/kohsuke/anaconda3/lib/python3.13/site-packages
>   ../../../bin/smart-tests
> ```
>
> Concatenate two paths to obtain the location, in the example above, that'd be `/home/kohsuke/anaconda3/lib/python3.13/site-packages/../../../bin/smart-tests`, which is `/home/kohsuke/anaconda3/bin/smart-tests`
>
> Add the directory portion of this to `PATH` by trimming the trailing `smart-tests`, like this:
>
> ```
> export PATH=/home/kohsuke/anaconda3/bin:$PATH
> ```

## (Optional) Install Jenkins plugin
If your CI system is Jenkins, you can install [the Smart Tests Jenkins plugin](launchable.hpi) to your Jenkins
and have it send your test results to Smart Tests. During the workshop, we will look at the data it collected to
reveal actionable insights to manage & improve your test suite.

When installed and configured, the plugin will automatically send test results Jenkins is seeing to Launchable
via its `junit` and other compatible steps.

Post installation, you need to go to system configuration screen to set the API token.
