## Pre-requisites
Install aws cli
Install docker
DynamoDB - Create a new table with name=students_marks_sheet , partiton_key=student_name and sort_key=marks

## To configure new profile
aws configure --profile test01

## To list all profiles
aws configure list-profiles

## To check which profile is active
 $env:AWS_PROFILE

## To check desired profiles
 $env:AWS_PROFILE = "myprofile"

## To build docker
docker build -t students_marks .

## To run docker locally
docker run -d -p 80:80 -e table_name=students_marks_sheet -e region=ap-southeast-1 --name student_app1 students_marks

## Access the app locally
http://127.0.0.1/

## Tag image and push
docker tag students_marks:latest 211125477393.dkr.ecr.ap-southeast-1.amazonaws.com/students_marks:latest
docker push 211125477393.dkr.ecr.ap-southeast-1.amazonaws.com/students_marks:latest