# Email Automation System 

### Main Idea: 
 To reduce the hassle of filtering out job related mails from your inbox. This project provides you a unified platform with gmail integration where you can easily find the mails.

## Current progress 
 Developing this project using Python, fast-api, postgresql 
 ### Status: 
* Initialized fast-api backend
* Added database connection, models (the table and necessary columns), schemas

* Added analytics and email routes and updated main.py accordingly
* Added ML layer with 44 samples that contain some real and synthetic data to train the ml model. 
* Making use of TF-IDF and logistic regression. 

### Current Trade-ofs: 
On very little data model has be trained on. Current dataset has only the body and the label, but an email has "Re:", "Fwd:", Long reply chains, Signatures, HTML artifacts. So modifying dataset will be done. 

#### Future enhancements under progress, please wait!