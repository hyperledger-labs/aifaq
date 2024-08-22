# CONTRIBUTION GUIDELINES
Welcome to the Hyperledger Labs AIFAQ project! We're excited to have you contribute and help us improve our project. Below are the guidelines to ensure a smooth and efficient contribution process.

## Code of Conduct
Please adhere to our [Code of Conduct](https://wiki.hyperledger.org/pages/viewpage.action?pageId=41587043). This code of conduct outlines our expectations for participants within the community as well as steps to report unacceptable behavior.

## Getting Started

### Frontend 
First, run the development server:

1.Clone the repository:
```bash 
git clone https://github.com/hyperledger-labs/aifaq.git
cd aifaq/frontend
```

2.Install dependencies:
```bash
yarn install
```

3.Start the developemnt server:
```bash
yarn dev
```

4.Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

### Backend

This software needs GPU for the execution, if you do not have a local GPU you could use a Cloud GPU.Run the AIFAQ API through [lighning.ai](https://lightning.ai/studios) after signup/login, create new Studio (project):

![New Studio Button](/images/new_studio.png)

select the left solution:

![Select Studio Code](/images/studio_code.png)

click on the **Start** button, and rename the new Studio:

![Rename Studio](/images/rename_studio.png)

Then, and copy-paste the github api repo code:

![Copy Paste Code](/images/copy_paste_code.png)

and create two folders:

1. chromadb (it will contains vector database files)
2. rtdocs (it will contains the ReadTheDocs documentation)

That version works with Hyperledger fabric documents (Wiki and ReadTheDocs).

## Usage

### Download ReadTheDocs documentation

Open a new terminal:

![Open Terminal](/images/open_terminal.png)

and download the documentation executing the command below:

```console
wget -r -A.html -P rtdocs https://hyperledger-fabric.readthedocs.io/en/release-2.5/

```

actually, after a minute we can interrupt (CTRL + C) because it starts to download previous versions:

![Wget Command](/images/wget_rtdocs.png)

Now, we can move into rtdocs folder and move the **release-2.5** content to **rtdocs**. We need to compress the content of the folder, moving there and use that command:

![Compress files](/images/compress_files.png)

and move the readthedocs.tar.gz to the parent directory (../):

```console
- mv readthedocs.tar.gz ..
- cd ..
```

repeating the two commands until we are into rtdocs folder:

![Move Command](/images/move_command.png)

now remove hyperledger… folder and the content:

![Compress files](/images/remove_command.png)

uncompress the file here and remove compress file:

```console
- tar -xzvf rtdocs.tar.gz
- rm rtdocs.tar.gz
```

### Install requirements

Move to the parent folder and execute the command below:

```console
pip install -r requirements.txt
```

### Activate GPU

After the requirements installation we can switch to GPU before to execute the ingestion script:

![Activate GPU](/images/activate_gpu.png)

then select the L4 solution:

![Select L4](/images/select_L4.png)

and confirm (it takes some minutes).

### Ingest step

Run the ingest.py script:

![Run Ingest](/images/run_ingest.png)

it will create content in chromadb folder.

### Run API

Now, we can run the API and test it. So, run api.py script:

![Run API](/images/run_api.png)

and test it:

```console
curl --header "Content-Type: application/json" --request POST --data '{"text": "How to install Hyperledger fabric?"}' http://127.0.0.1:8080/query
```

below the result:

![Show results](/images/curl_results.png)

## How to Contribute
### Fork the repository

- Navigate to the [repository on GitHub](https://github.com/hyperledger-labs/aifaq).

- Click the "Fork" button in the top right corner

### Create a New Branch
- Clone your forked repository:

```bash
git clone https://github.com/your-username/aifaq.git
cd aifaq/frontend
```
- Create a new branch for your feature or bug fix:

```bash
git checkout -b feature-branch
```
### Make Your Changes

- Make the necessary changes in your local repository.

- Ensure your code adheres to our Code Style guidelines.

### Commit Your Changes
- Stage your changes:

```bash
git add .
```
- Commit your changes with a descriptive message:

```bash
git commit -m 'Add some feature'
```
### Push to the Branch
- Push your changes to your forked repository:

```bash
git push origin feature-branch
```
### Open a Pull Request
- Navigate to your forked repository on GitHub.

- Click the "New pull request" button.

- Provide a detailed description of your changes and submit the pull request.

### Pull Request Guidelines

1.Ensure your pull request (PR) is up to date with the main branch.

2.Provide a detailed description of the changes in your PR.

3.Link any related issues in your PR description.

4.Ensure your code passes all tests and adheres to the project's coding standards.

5.Be responsive to feedback and be prepared to make necessary changes.

6.We value all contributions, but please be aware that low-effort PRs, such as those lacking thorough testing, proper documentation, or a clear and meaningful purpose, may not be accepted. Please ensure your PR is well-considered and adds value to the project.


```


### Issue Reporting
If you encounter any issues or bugs, please report them by following these steps:

1.Navigate to the Issues section of the repository.

2.Click on "New Issue."

3.Provide a descriptive title and detailed description of the issue.

4.Include any relevant screenshots or error messages.

5.Assign appropriate labels (e.g., bug, enhancement, question).

### Community and Support
Join our community meetings every Monday. The invitation is on the Hyperledger Labs calendar: [Hyperledger Labs Calendar](https://wiki.hyperledger.org/display/HYP/Calendar+of+Public+Meetings).

For additional support, you can reach out on our Hyperledger Chat on [Discord](https://discord.gg/hyperledger).
