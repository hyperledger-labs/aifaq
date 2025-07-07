# Contributing to AIFAQ

## Introduction

AIFAQ is an open-source project under Linux Foundation Decentralized Trust umbrella. It aims to build an AI Chatbot to support newby in communities (companies, organizations, individuals, …).
This guide allows the AIFAQ community to contribute activities. Please, read before starting coding.

## Prerequisites

Join the [weekly meetings](https://zoom-lfx.platform.linuxfoundation.org/meeting/96156160446?password=436922cc-9811-4e05-aa60-04f7b4679c7e) on Monday at 9 am EST time zone.

## Code of Conduct and Antitrust Policy

- [Linux Foundation Privacy Policy](https://www.linuxfoundation.org/legal/privacy-policy)
- [Terms of use](https://www.linuxfoundation.org/legal/terms)
- [Antitrust Policy](https://www.linuxfoundation.org/legal/antitrust-policy)
- [Code of Conduct](https://www.lfdecentralizedtrust.org/code-of-conduct)

## GitHub Flow

Please select a task from the [published issues](https://github.com/hyperledger-labs/aifaq/issues); other changes will not be considered. For improvement proposals, kindly attend the [Monday meetings](https://zoom-lfx.platform.linuxfoundation.org/meeting/96156160446?password=436922cc-9811-4e05-aa60-04f7b4679c7e).
Below the GitHub tree:

<img src="../images/github_tree.png" alt="GitHub tree"/>

and the workflow schema:

<img src="../images/workflow.png" alt="GitHub workflow"/>

We should document all changes describing the solution and adding screenshots or a short video (like [this](https://github-production-user-asset-6210df.s3.amazonaws.com/190102379/461524193-6ee9ee0c-2cd1-4ab3-97ea-904515cd5b6c.webm?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250704%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250704T111312Z&X-Amz-Expires=300&X-Amz-Signature=e9ba00009ffd4bd997e34a62a5a5ff647e845bd7786790c495318de77b446737&X-Amz-SignedHeaders=host)).

## Commands

In your local PC, create a new folder and open it in VS Code.
Then open a new terminal:

<img src="../images/new_terminal.png" alt="VS Code new terminal"/>

go to [AIFAQ GitHub repo agents branch](https://github.com/hyperledger-labs/aifaq/tree/agents) and press on fork button:

<img src="../images/fork_button.png" alt="GitHub fork button"/>

uncheck that checkbox and press on create fork button:

<img src="../images/create_fork.png" alt="GitHub create fork"/>

it will create a fork in your local GitHub space.

<img src="../images/copy_url.png" alt="GitHub copy url repo"/>

Then click on the code button and copy the https url to clipboard:

Now, type

```console
git clone https://github.com/gcapuzzi/aifaq.git
```

on vs code terminal:

<img src="../images/git_clone.png" alt="git clone terminal command"/>

now we can move to the aifaq folder:

```console
cd aifaq
```

and list the current branches:

```console
git branch -a
```

<img src="../images/git_branch_a.png" alt="git branch -a terminal command"/>

we can see that the current branch is **main** and it refers to the **remote main branch**.
But, we want to change a different branch (in our case, mvt-streamlit branch) so execute:

```console
git checkout origin/mvt-streamlit
```

<img src="../images/git_checkout_origin.png" alt="git checkout origin terminal command"/>

and execute

```console
git branch -a
```

in order to check the current remote branch.

Ok, now we can create a new local branch with same name:

```console
git checkout mvt-streamlit
```

<img src="../images/git_checkout.png" alt="git checkout terminal command"/>

and

<img src="../images/git_branch2.png" alt="git branch terminal command"/>

and now we can do our dev activities.
In my case, I want to add a new file (faiss_content_py) with copy-paste.
When I finish my changes, type:

```console
git status
```

<img src="../images/git_status.png" alt="git status terminal command"/>

so, we have to commit our changes before to push those to the remote branch:

```console
git add -A
git commit -s -m “Added faiss_content.py file”
```

<img src="../images/git_add_commit.png" alt="git add commit terminal command"/>

The first command adds the changes to the commit and the second one executes the commit (please check the ‘-s’ argument that is mandatory in Linux Foundation).

Now, we can push the code to the remote branch:

```console
git push -u origin mvt-streamlit
```

<img src="../images/git_push_origin.png" alt="git push origin terminal command"/>

now if we check our mvt-streamlit branch in the personal GitHub space:

<img src="../images/mvt_streamlit.png" alt="mvt-streamlit GitHub branch"/>

## Pull Request

The changes are in our GitHub space, but we want the same in the official project repo. So open a **Pull Request**:

<img src="../images/new_pull_request.png" alt="GitHub new pull request"/>

and set up the two branches:

<img src="../images/select_branches.png" alt="GitHub new pull request select branches"/>

then click on **Create pull request button**:

<img src="../images/open_pull_request.png" alt="GitHub open pull request"/>

Please add a short description and click on the **Create pull request button**.
And remove the branch:

<img src="../images/remove_branch.png" alt="GitHub remove branch"/>
