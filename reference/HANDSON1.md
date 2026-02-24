# Lab 1. Environment setup

First, locally clone the repositories you want to try Smart Tests with.
If your test and production code reside in two different repositories, clone both of them.

If your production code are split among multiple repositories, we recommend you clone a couple of major ones, just to keep this workshop manageable.

## Obtain an API token

You need an API token to use Smart Test.
Go to your workspace’s Settings > API Token and generate a new token.

**Node:** If you haven’t created a workspace yet, please refer to [SIGN_UP.md](SIGN_UP.md) to set one up.

<img src="https://github.com/user-attachments/assets/e57fad93-6da6-4eb1-aa37-da2c139804a4" width="50%" />

<br>

Click **Copy** key and copy API key.

<img src="https://github.com/user-attachments/assets/5025328b-fc20-4eb1-b7f2-346aab60e013" width="50%">

The `smart-tests` command expects an API token to be set in the `SMART_TESTS_TOKEN` environment variable.

```sh
export SMART_TESTS_TOKEN=<API TOKEN>
```


## Make sure everything is in order

`smart-tests verify` command is a convenient way to make sure all the prerequisites are met and the API key is valid:

```
smart-tests verify
```

If you see a message like this, you're all set:

```
Organization: 'organization'
Workspace: 'workspace'
Proxy: None
Platform: 'Linux-6.10.14-linuxkit-aarch64-with-glibc2.36'
Python version: '3.11.13'
Java command: 'java'
smart-tests version: '2.2.0'
Your CLI configuration is successfully verified 🎉
```

___

If you see the help message, the installation was successful.
You can now move on to [the next step](HANDSON2.md).



