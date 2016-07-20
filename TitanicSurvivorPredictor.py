import urllib2
# If you are using Python 3+, import urllib instead of urllib2
import re
import json


AccoClass = raw_input('Enter Accomodation Class(1,2,3): ')
Sex = raw_input('Enter Sex As(male or female): ')
Age = raw_input('Enter your age in numbers(0 -115): ')
SibSpouse = raw_input('Enter the # of Sibling/Spouse traveling (in numbers): ')
Parch = raw_input('Enter # of children traveling (in numbers): ')
Fare = raw_input('Enter the fare you paid(in numbers): ')
embark = raw_input('Enter the place of embark(S,C,Q): ')

data =  {

        "Inputs": {

                "input1":
                {


                    "ColumnNames": ["AccomodationClass", "Sex", "Age", "SiblingSpouse", "ParentChild", "Fare", "Embarked"],
                    "Values": [ [ AccoClass, Sex, Age, SibSpouse, Parch, Fare, embark ], [ AccoClass, Sex, Age, SibSpouse, Parch, Fare, embark ], ]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/79e371616c4d480a8b693cde553275a7/services/e04b11994bcf40c6ac74de5c931d10f4/execute?api-version=2.0&details=true'
api_key = 'JFYoJmEFf6h+TFtZxpLUMdlEqsXf6MV2KQmZWfgmwsLVzFVOVt+JqaIu13EehNjnM3uq3LprVmliVE8OYH328g==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib2.Request(url, body, headers)

try:
    response = urllib2.urlopen(req)

    result = response.read()

    probability= re.findall('0.\d+', result)

    probability=float(probability[0])*100
    probability=round(probability,ndigits=0)

    print("The probability of your survival is: %0.0f" %probability +"%")

except urllib2.HTTPError, error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))