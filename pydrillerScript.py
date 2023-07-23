#!pip install pydriller  #installing the pydriller packgage.

#importing the require libraries / packages.
import pydriller as py
import re
import requests
import time
import csv
import pandas as pd
import ast

# Note: replace 'YOUR_GITHUB_TOKEN' with your GitHub personal access token.
headers = {
    'Authorization': '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',
    'Accept': 'application/vnd.github.v3+json',
}

params = {
    'q': 'topic:chess language:java',
    'sort': 'stars',  # Sort by stars
    'order': 'desc',  # Order by descending
    'per_page': 200,  # Max results per page
}


url = 'https://api.github.com/search/repositories'


# This function uses a regular expression to extract Java function definitions from Java code.
#  It returns a list of tuples, where each tuple contains the entire match and individual groups.

def extract_functions(java_code):
    # Warning: This regex is highly simplified and will not correctly handle many real-world cases!
    functions = re.findall(r"((public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(\w+) *\([^\)]*\) *\{[^}]*\})", java_code, re.MULTILINE | re.DOTALL)
    return functions  # This will return a list of tuples where each tuple contains the entire match and the individual groups



# This function checks if a given function name matches the target function name. 
# By default, the target function name is 'move'.

def is_target_function(function_name, target='move'):
    return function_name.lower() == target.lower()



# This function retrieves function data and commit counts from a given GitHub repository URL. 
# It uses PyDriller to traverse the commits and extract relevant information.

def get_functions(gitURL):
    function_data = []  # list to store function data
    commit_counts = {}  # dictionary to store commit count for each file
    for commit in py.Repository(gitURL).traverse_commits():
        for modification in commit.modified_files:
            if modification.filename.endswith('.java') and modification.change_type is not None and modification.source_code is not None:
                functions = extract_functions(modification.source_code)
                target_functions = [f for f in functions if is_target_function(f[2])]  # f[2] is the function name
                for function in target_functions:
                    # store the data in a dictionary
                    function_info = {
                        'Function': function[2],
                        'Commit': commit.hash,
                        'Filename': modification.filename,
                        'Method code': function[0],
                        'URL': gitURL
                    }
                    function_data.append(function_info)
                    # increment commit count for the file
                    if modification.filename in commit_counts:
                        commit_counts[modification.filename] += 1
                    else:
                        commit_counts[modification.filename] = 1
    return function_data, commit_counts


# This function searches for GitHub repositories based on a specified query using the GitHub API. 
# It returns a list of repository URLs.

def get_gits_projects(project_number):
    global url  # Declare url as global
    count = 0
    repo_urls = []  # Create an empty list to hold the URLs
    while count < project_number:
        response = requests.get(url, headers=headers, params=params)

        # Check the status of the request
        if response.status_code != 200:
            print(f"Failed to get response, status code: {response.status_code}")
            break

        data = response.json()

        # Extract the URL from each repository
        for repo in data['items']:
            if count < project_number:
                repo_url = repo['html_url']
                #print(repo_url)
                repo_urls.append(repo_url)  # Append the URL to the list
                count += 1
            else:
                break

        # Check if there is a next page
        if 'next' not in response.links or count >= project_number:
            break

        # Get the URL for the next page
        url = response.links['next']['url']

        # Sleep for a while to avoid hitting the rate limit
        time.sleep(10)

    return repo_urls  # Return the list of URLS


def get_functions_by_list(urls):
  for git_url in urls:
    get_functions(git_url)


# This function writes data to a CSV file with the provided filename and field names.

def write_to_csv(data, filename, fields):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(data)


# This function is the main driver function that runs the entire project. 
# It searches for GitHub repositories, extracts function data, and writes the results to CSV files.
def run(project_number):
    urls = get_gits_projects(project_number)
    function_data = []  # list to store all function data
    commit_counts = []  # list to store commit count data
    for url in urls:
        function_info, commit_count = get_functions(url)  # get the function data and commit count for each url
        function_data.extend(function_info)  # extend the function data list
        commit_counts.append({'Repository': url, 'Commit Count': commit_count})  # add commit count to list
    write_to_csv(function_data, 'function_data.csv', ['Function', 'Commit', 'Filename', 'Method code', 'URL'])  # write the function data to a CSV file
    write_to_csv(commit_counts, 'commit_counts.csv', ['Repository', 'Commit Count'])  # write the commit counts to a separate CSV file



#CSVfiles
commFile = 'commit_counts.csv'
funcFile = 'function_data.csv'

outputFile = 'longest_methods.csv'  # Name of the output file
resultFile = 'result.csv'  # Specify the path/name of the result file



# This function reads function data from a CSV file, groups it by repository URL,
#  and finds the longest method code for each repository.
#  It then writes the results to a new CSV file.

def get_longest_method_code(filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Group the data by URL
    grouped = df.groupby('URL')

    # Initialize a list to store the longest method code for each URL
    longest_methods = []

    # Iterate over each group
    for url, group in grouped:
        # Sort the group by the length of the method code in descending order
        sorted_group = group.sort_values(by='Method code', key=lambda x: x.str.len(), ascending=False)

        # Get the first row (longest method code) from the sorted group
        longest_method = sorted_group.iloc[0]

        # Append the longest method code to the list
        longest_methods.append(longest_method)

    # Create a new DataFrame from the longest methods list
    result_df = pd.DataFrame(longest_methods)

    # Write the result DataFrame to a new CSV file
    result_df.to_csv('longest_methods.csv', index=False)



# This function reads commit count data from a CSV file and removes rows with empty commit counts.
#  It writes the modified data to a new CSV file.

def delete_invalid_commit_counts(filename):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Delete rows with "{}" values in the Commit Count column
    df = df[df['Commit Count'] != '{}']

    # Write the modified commit count DataFrame to a new CSV file
    new_filename = 'modified_' + filename
    df.to_csv(new_filename, index=False)

    # Return the new filename
    return new_filename


finalFile = 'final_result.csv'


#This function reads data from two CSV files (unique functions and commit counts), 
# merges them based on repository URLs, and writes the final result to a new CSV file.

def merge_and_write_dataframes(unique_file, commit_file, final_file):
    # Read the unique file into a DataFrame
    df_unique = pd.read_csv(unique_file)

    # Read the commit file into a DataFrame
    df_commit = pd.read_csv(commit_file)

    # Merge the unique and commit DataFrames on 'URL' and 'Repository' columns
    df_merged = pd.merge(df_unique, df_commit, left_on='URL', right_on='Repository')

    # Select the desired columns
    df_final = df_merged[['URL', 'Method code', 'Filename', 'Function', 'Commit Count']]

    # Write the final result DataFrame to a CSV file
    df_final.to_csv(final_file, index=False)


# This function reads data from a CSV file, matches rows based on filenames and commit counts, 
# and writes the matched rows to a new CSV file.
def match_and_write_rows(filename):
    # Read the input file into a DataFrame
    df_final = pd.read_csv(filename)

    # Create a new DataFrame to store the matched rows
    matched_rows = pd.DataFrame(columns=df_final.columns)

    # Iterate over each row in the DataFrame
    for index, row in df_final.iterrows():
        commit_count = row['Commit Count']
        filename = row['Filename']

        # Convert the commit count string to a dictionary
        try:
            commit_count_dict = ast.literal_eval(commit_count)
        except (ValueError, SyntaxError):
            continue

        # Check if the filename exists as a key in the commit count dictionary
        if filename in commit_count_dict:
            commit_count_value = commit_count_dict[filename]
            row['Commit Count'] = commit_count_value
            matched_rows = matched_rows.append(row)

    # Write the matched rows to a new CSV file
    matched_file = 'matched_result.csv'
    matched_rows.to_csv(matched_file, index=False)


#Calling methods->
#searching a Github repositories in topic: chess, language:java
run(250)

# Read the CSV file into a DataFrame
df_com = pd.read_csv(commFile)
df_func = pd.read_csv(funcFile)

# Call the function with the filename of the function_data.csv file
get_longest_method_code('function_data.csv')
# Read the CSV file into a DataFrame
df_unique = pd.read_csv(outputFile)

# Call the method with the filename of the commit_counts.csv file
new_filename = delete_invalid_commit_counts('commit_counts.csv')
print(f"Modified commit counts saved to: {new_filename}")

delete_invalid_commit_counts(commFile)


# Call the method with the filenames
merge_and_write_dataframes('longest_methods.csv', 'modified_commit_counts.csv', 'final_data.csv')

# Call the method with the filename of the final_result.csv file
match_and_write_rows('final_data.csv')
