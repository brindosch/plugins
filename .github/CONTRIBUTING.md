# Hyperion Plugins Contributing Guide

Hi! I’m really excited that you are interested in contributing to Hyperion Plugins. Before submitting your contribution though, please make sure to take a moment and read through the following guidelines.

- [Issue Reporting](#issue-reporting)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Development](#develope-a-plugin)

## Issue Reporting
This repository has no issue tracker.
If you have issues with a plugin please visit our forum or follow the support url that each plugin provides. Feature requests are also possible. [hyperion-project.org](https://hyperion-project.org/forums/plugins-support.36/)

## Pull Request Guidelines

- All plugins are served in the `master` branch, this is also the place where your pull request should go to.

- A Pull Request title should have the following syntax `[pluginID] V MAJOR.MINOR.PATCH` Example: `[service.sample] V1.0.5`

- [Travis CI](https://travis-ci.org) will test each pull request against common mistakes or pitfalls which will break the functionality. This test runs on each commit (duration of ~1 minute), to let the test know which plugin it should test please add to each commit message (can be comment or title) your plugin id in `[]` eg. `[service.sample]`. **A PR with failed test result can't be merged**

- It's OK to have multiple small commits as you work on the PR - we will let GitHub automatically squash it before merging. But keep in mind that each commit message (from the point you opened the pull request) needs to contain the plugin id of your plugin in `[]` eg. `[service.sample]` to execute the travis test

- One Pull Request should touch only one plugin folder, not multiple ones. Our publish system is automated, so you need to seperate them.

- After your Pull Request has been merged, the update will be available after ~1 minute. The rollout will happen during the next 24 hours to all running hyperion instances

## Develope a Plugin

Please read here: [Plugin development](https://docs.hyperion-project.org/en/developer/plugins#plugin_development)
