from techharper import GitHubService
import json
import argparse

""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.

Credit: https://stackoverflow.com/questions/18478287/making-object-json-serializable-with-regular-encoder/18561055#18561055
"""
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default # Replace it.

def writeOutput(results: dict, outputMethod: str):
    if(outputMethod == 'json'):
        json_object = json.dumps(results, indent = 4) 
        with open('output.json', 'w') as file:
            file.write(json_object)
    if(outputMethod == 'console'):
        print(json.dumps(results, indent = 4))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True, help="GitHub Personal Access Token")
    parser.add_argument("--repository", required=True, help="GitHub repository in form `vercel/next.js`")
    parser.add_argument("--since", help="(Optional) Filter results to only items since date in format yyyy-MM-dd")
    parser.add_argument("--output", help="(Optional) Specify where to output. Options: [console, json]")
    
    args = parser.parse_args()
    if not args.token:
        print('Please retry with a GitHub PAT token specified with the `--token TOKEN` argument')
        return
    
    if not args.repository:
        print('Please retry with a GitHub repository specified with the `--repository REPOSITORY` argument')

    outputMethod = args.output
    if(outputMethod is None):
        outputMethod = 'console'
    if(outputMethod != 'json' and outputMethod != 'console'):
        print('Please retry with a valid output argument `--output json` or `--output console')
        return

    service = GitHubService(args.token)
    results = []
    repository = args.repository
    result = service.generateNotification(repository, sinceDate=args.since)
    if(result is not None):
        results.append(result)
    writeOutput(results, outputMethod)

if __name__ == "__main__":
    main()
