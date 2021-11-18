![Stability](https://img.shields.io/badge/Stability-Beta-yellowgreen) ![Version](https://img.shields.io/badge/Version-Beta-brightgreen) ![Python](https://img.shields.io/badge/Python-3-blue)
![Docker Pulls](https://img.shields.io/docker/pulls/bughound/bughound)

# What is Bughound?

![Bughound Logo](https://shells.systems/wp-content/uploads/2021/01/Bughound-Logo.png)


Bughound is an open-source static code analysis tool that analyzes your code and sends the results to Elasticsearch and Kibana to get useful insights about the potential vulnerabilities in your code.

Bughound has its own Elasticsearch and Kibana Docker image that is preconfigured with dashboards to give you a strong visualization for the findings.

Also you can use docker compose file for running Elasticsearch and Kibana in Your machine without Dockerising this tool

You can detect various types of vulnerabilities such as:
* Command Injection.
* XXE.
* Unsafe Deserialization.
* And more!

Bughound can analyze `PHP` and `JAVA` code for now, and it contains a group of unsafe functions for these languages.

I will make sure to add more and more functions/languages coverage with time, but for now the main focus is for the project stability itself.


***Please note that Bughound results are not 100% accurate, it built to help you identify potential weaknesses during your analysis to investigate.***



# How it works?

First of all, Bughound will build a list of all the files inside your project based on the extension of the files you want to audit, then it will read each file and try to find any pre-defined unsafe functions for your project's language.

The analysis phase depends on pre-configured regex and some custom text matching to detect the potential vulnerabilities, so again, you need to do the manual analysis so you can check if these findings are exploitable.

Finally, it will send the results to the Bughound docker image which has a pre-configured Elasticsearch and Kibana that contain the customized dashboards for your findings.

The dashboards will give you details about the findings such:
* Function name.
* Category of the vulnerability.
* Line number.
* And much more!

Also using Kibana, you will be able to view the potentially vulnerable code snippet to start doing your analysis and tracing phase to check if it's exploitable or not.

Of course, you can use your own ELK stack if you want, and Bughound will do the initial configuration for you, but you will not have the pre-configured dashboards in this case.


# Requirements

You can install all the requirements to run Bughound code using the following command:

`pip3 install -r requirements.txt`

That will make sure all the requirements are installed for the code.

Also, you need to [install Docker](https://docs.docker.com/engine/install/) in order to run the Bughound image, more regarding this in the next section!

**If you want to use your own Elasticsearch and Kibana instances, skip the docker installation step**



# Installation

Make sure to get the latest version of Bughound using the following command:

`git clone https://github.com/mhaskar/Bughound`

And after installing the requirements in the previous step you can run Bughound using the following command:

`./bughound.py`


### Docker image installation

To install the Bughound docker image, you can simply do the following:

`docker pull bughound/bughound`

And that will pull the latest version of the image and save it to your machine.

Once we pulled the image, we can run it using the following command:

`docker run --name bughound -p5601:5601 -p 9200:9200 bughound/bughound`

That will run the image under a new container called `bughound` and expose the ports that are needed by Bughound to communicate Elasticsearch and Kibana to your host.

You may need to increase the max virtual memory in order to use the image, so please make sure to run this command:

`sysctl -w vm.max_map_count=262144`

After getting two things done, you are ready now to use Bughound!

# Usage

To start the analysis process for your code, you should use `Bughound.py` file which has some options, to see these options via the help banner, you can use the following command:

```
usage: bughound.py [-h] [-p PATH] [-g GIT] [-elk] -l LANGUAGE [-e EXTENSION]
                   [-n NAME] [-v] [-j] [-o OUTPUT]

Example: ./bughound3.py --path vulnerable_code/ --language php --extension
.php --name test_project

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Local path of the source code
  -g GIT, --git GIT     GitHub repository URL
  -elk, --use-elastic   initialize Elastic and Kibanna requirements. -n/--name
                        argument required
  -l LANGUAGE, --language LANGUAGE
                        Used programming language
  -e EXTENSION, --extension EXTENSION
                        File extension for analyze. Default for Java - .java
                        Default fpr PHP - .php
  -n NAME, --name NAME  Project name to use in Elasticsearch and Kibanna
  -v, --verbose         show debugging messages
  -j, --json            Print found data in json format
  -o OUTPUT, --output OUTPUT
                        Print found data to file
```

## Finding Output example

If you don't use Elasticsearch tool will print found data in this way

```
----------------------------------------------------------------------------------------------------
Found SQL injection
File: /home/nikolai/Downloads/targets/targets_backup/DVWA-master/dvwa/includes/DBMS/PGSQL.php
Line: 93
Code:
// Insert data into 'guestbook'
$insert = "INSERT INTO guestbook (comment, name) VALUES('This is a test comment.','admin')";

if( !pg_query( $insert ) ) {
	dvwaMessagePush( "Data could not be inserted into 'guestbook' table<br />SQL: " . pg_last_error() );
	dvwaPageReload();
}

----------------------------------------------------------------------------------------------------
```

## Scan Local project
For example, to scan a local php project, you can use the following command:

`./bughound.py --path /opt/dummyproject --language php`

This command will crawl all the local files with the extension ".php" in the local path "/opt/dummyproject" and prind found data.

## Scan remote git repository
Also, you can pull a remote project from git repository using `--git` switch like the following:

`./bughound.py --git https://github.com/DummyCode/DummyProject --language php`

Bughound will clone the code for you and save it in `projects` directory, then will scan it.

## Extensions
You can use argument `-e\--extension` for specifying extension for scan. Like `.git` or `.java`.

## Elasticsearch support
For using this script with elasticsearch, you need to enable it with argument `-elk/--use-elastic` and choose project name with `-n/--name dummyproject`.

## Json support
You can use `-j\--json` for converting findings to json

## Output files support
You can use `-o\--output FILE.extension` for writing found data to file. 

Example: `FILE.txt` or `FILE.json`

# Preconfigured Dashboards

If you decided to use the official Bughound docker image, you will get a couple of ready to use dashboards that will help you to do your analysis.

The following dashboards are available so far:
* Bughound main dashboard
* Command injection dashboard
* Deserialization dashboard
* XXE dashboard

These dashboards will give you statistics about the functions and code snippets that was found in the code so you can start your analysis process.

# More resources

For more information about Bughound check the following articles:
* [Unveiling BugHound: a static code analysis tool based on ElasticSearch](https://shells.systems/unveiling-bughound-a-static-code-analysis-tool-based-on-elasticsearch)


# License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details
