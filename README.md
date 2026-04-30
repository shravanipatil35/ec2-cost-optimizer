# 🚀 EC2 Cost Optimizer (AWS)

## 📌 Overview

This project automatically stops unused EC2 instances to save cost and starts them at a scheduled time.

## 🛠 Services Used

* AWS Lambda
* Amazon EventBridge
* Amazon EC2
* Amazon CloudWatch
* Amazon DynamoDB

## ⚙️ How It Works

* EventBridge triggers Lambda every 5 minutes
* Lambda checks CPU usage using CloudWatch
* If CPU < 5% → instance stops
* At 9 AM UTC → instance starts
* Only instances with tag `AutoStop = true` are affected
* All actions are logged in DynamoDB

## 📊 Features

* Automated cost optimization
* Tag-based control
* Start + Stop scheduling
* Logging system

## 🧪 Sample Output

* Instance stopped when CPU is low
* Instance started at scheduled time
* Logs stored in DynamoDB

## 📷 Architecture

(EventBridge → Lambda → EC2 + CloudWatch → DynamoDB)

## 💡 Future Improvements

* Dashboard UI
* Notifications
* Multi-region support

---
