import argparse
import docker
import duckdb
import glob
import os
import random
import re
import sys
import subprocess
import textwrap
from shared_functions import fetch_data
from shared_functions import sha_matching
from shared_functions import list_extensions
from shared_functions import get_full_sha
from verify_python_build import verify_and_test_python_linux

GH_REPO = os.environ.get('GH_REPO', 'duckdb/duckdb')
GH_COMMUNITY_EXTENSIONS_REPO = 'duckdb/community-extensions'
ACTIONS = ["INSTALL", "LOAD"]
EXT_WHICH_DOESNT_EXIST = "EXT_WHICH_DOESNT_EXIST"
SHOULD_BE_TESTED = ('python', 'osx', 'linux', 'windows')

def list_community_extensions_from(repo):
    result = subprocess.run(["gh", "api", f"repos/{GH_COMMUNITY_EXTENSIONS_REPO}/contents/extensions", "--paginate", "--jq", ".[].name"], capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def list_community_extensions_s3(release_tag, platform): 
    result = subprocess.run(["aws", "s3", "ls", "--recursive", f"duckdb-community-extensions/{release_tag}/{platform}/"], capture_output=True, text=True)
    raw_list = result.stdout.strip().splitlines()
    clean_list = []
    for item in raw_list:
        match = re.search(rf'{platform}/([^/]+)\.duckdb_extension\.gz', item)
        if match:
            clean_list.append(match.group(1))
    return clean_list 

def main():
    release_tag = "v1.2.2"
    print("List of community extensions from GitHub:\n", list_community_extensions_from(GH_COMMUNITY_EXTENSIONS_REPO))
    print(len(list_community_extensions_from(GH_COMMUNITY_EXTENSIONS_REPO)))
    print(f"List of community extensions from S3 bucket with the release tag {release_tag}:\n", list_community_extensions_s3(release_tag, "linux_amd64"))
    print(len(list_community_extensions_s3(release_tag, "linux_amd64")))
    print("Diff - extensions on GH not found on S3:\n", list(set(list_community_extensions_from(GH_COMMUNITY_EXTENSIONS_REPO)) - set(list_community_extensions_s3(release_tag, "linux_amd64"))))
    print("Diff - extensions on S3 not found on GH:\n", list(set(list_community_extensions_s3(release_tag, "linux_amd64")) - set(list_community_extensions_from(GH_COMMUNITY_EXTENSIONS_REPO))))
    
if __name__ == "__main__":
    main()