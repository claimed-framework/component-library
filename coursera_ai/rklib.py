import requests, json

def submit(submitterEmail,secret,key,submission_part, all_parts, data):
        submission = {
                    "assignmentKey": key,
                    "submitterEmail":  submitterEmail,
                    "secret":  secret,
                    "parts": {}
                  }
        for part in all_parts:
            if part == submission_part:
                submission["parts"][part] = {"output": data}
            else:
                submission["parts"][part] = dict()
        response = requests.post('https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1', data=json.dumps(submission))
        if response.status_code == 201:
            print ("Submission successful, please check on the coursera grader page for the status")
        else:
            print ("Something went wrong, please have a look at the reponse of the grader")
            print ("-------------------------")
            print (response.text)
            print ("-------------------------")
            
def submitAll(submitterEmail,secret,key,parts_and_data):
        submission = {
                    "assignmentKey": key,
                    "submitterEmail":  submitterEmail,
                    "secret":  secret,
                    "parts": {}
                  }
        for part, output in parts_and_data.items():
            if output is not None:
                submission["parts"][part] = {"output": output}
            else:
                submission["parts"][part] = dict()
        response = requests.post('https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1', data=json.dumps(submission))
        if response.status_code == 201:
            print ("Submission successful, please check on the coursera grader page for the status")
        else:
            print ("Something went wrong, please have a look at the reponse of the grader")
            print ("-------------------------")
            print (response.text)
            print ("-------------------------")
