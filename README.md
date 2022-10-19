# avtMonMedExp project on Python 3


## 1. Introduction

The `avtMonMedExp` project using Amazon Comprehend Medical with Python3.

This project is a qualitatively new stage in the implementation of the  [avtMonExp](https://github.com/SP-Vita-Tolstikova/avtMonExp) project for Medical domain. Thanks to the use of modern natural language processing (NLP) tools from Amazon.

The `avtMonMedExp` project includes the following main stages in data processing:

1. First of all, search criteria (tags, phrases) that characterize the subject area and experts from the Medical domain are determined.

2. Search, retrieve, and analysis data about experts in Medical domain from Twitter based on pre-defined criteria.

3. Searching and analyzing experts from the field of medicine among Twitter users consists of two main stages:
     2.1  On the **first stage of data analysis**, an algorithm developed by A.V.T. Software is used to identify a Twitter user as an expert in a Medical domain.
     2.2 On the **second stage of data analysis**, we use Amazon Comprehend Medical DetectEntitiesV2 operation for analysis Twitter user data to identify specific medical entities. To more accurately understand whether the Twitter user whose data we are analyzing is an expert or a patient. 

4. Saves data about found experts from Medical domain that corresponds to the specified criteria in the relational database for future analysis, and visualization.

## 2. Requirements

### 2.1 The `avtMonMedExp` project requires the following **main components**:

* [Python 3.9.5](https://www.python.org/) - Python is a programming language that lets you work quickly
* [TwitterSearch 1.0.2 by Christian Koepp](https://pypi.python.org/pypi/TwitterSearch/) - A Python library to easily iterate tweets found by the Twitter Search API
* [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to configure, and manage AWS services, such as Amazon Comprehend Medical
* [Python Geocoder by DenisCarriere](https://github.com/DenisCarriere/geocoder) - Simple and consistent geocoding library written in Python
* [MySQL Community Server 5.7](https://dev.mysql.com/downloads/mysql/) - MySQL Community Edition is a freely downloadable version of the world’s most popular open source database that is supported by an active community of open source developers and enthusiasts
* [MySQL Connector/Python ](https://dev.mysql.com/downloads/connector/python/) - MySQL Connector/Python is a standardized database driver for Python platforms and development.


## 3. How to prepare and start using this project step by step

### 3.1 Fork, Clone or Download the project

### 3.2 Install the requirements

### 3.3 Create a MySQL database called `monexp_db`

### 3.4 Instead of data placeholders, add your real data to the following project files:

#### 3.4.1 Description of the domain model and experts using JSON. To search on Twitter and further analysis of search results

##### 3.4.1.1 Format of the `domains_data.json` file

```javascript
// avt-mon-med-exp/avt_mon_med_exp/domains_data.json

{
  "domains": [
    {
      "domain":"your_domain_1",
      "tags":{ // Tags are strings with no spaces, which describe the domain. 
               // The tags will perform in the following three forms:
               // 1. "your_tag"
               // 2. "#your_tag"
               // 3. "@your_tag"
        "your_tag_1_1":your_tag_score_1_1, // Your score for the tag is from 1 to 5
        "your_tag_1_2":your_tag_score_1_2,
        "your_tag_1_3":your_tag_score_1_3,
        ...
        "your_tag_1_n":your_score_1_n
       },
      "phrases":{ // Phrases are strings with spaces, which describe the domain.
        "your phrase_1_1":your_phrase_score_1_1, // Your score for the phrase is from 1 to 5
        "your phrase_1_2":your_phrase_score_1_2,
        "your phrase_1_3":your_phrase_score_1_3,
        ...
        "your phrase_1_m":your_phrase_score_1_m
      }, 
      "expert_keywords":{ // Expert keywords are strings without spaces, which describe experts 
                          // in the specified domain
        "your_expert_keywords_1_1":your_expert_keywords_score_1_1, //Your score for the expert keyword
                                                                   // is from 1 to 5
        "your_expert_keywords_1_2":your_expert_keywords_score_1_2,
        "your_expert_keywords_1_3":your_expert_keywords_score_1_3,
        ...
        "your_expert_keywords_1_k":your_expert_keywords_score_1_k
      }
    },
    {
      "domain":"your_domain_2",
      "tags":{ // Tags are strings with no spaces, which describe the domain. 
               // The tags will perform in the following three forms:
               // 1. "your_tag"
               // 2. "#your_tag"
               // 3. "@your_tag"
        "your_tag_2_1":your_tag_score_2_1, // Your score for the tag is from 1 to 5
        "your_tag_2_2":your_tag_score_2_2,
        "your_tag_2_3":your_tag_score_2_3,
        ...
        "your_tag_2_n":your_score_2_n
       },
      "phrases":{ // Phrases are strings with spaces, which describe the domain.
        "your phrase_2_1":your_phrase_score_2_1, // Your score for the phrase is from 1 to 5
        "your phrase_2_2":your_phrase_score_2_2,
        "your phrase_2_3":your_phrase_score_2_3,
        ...
        "your phrase_2_m":your_phrase_score_2_m
      }, 
      "expert_keywords":{ // Expert keywords are strings without spaces, which describe experts 
                          // in the specified domain
        "your_expert_keywords_2_1":your_expert_keywords_score_2_1, //Your score for the expert keyword
                                                                   // is from 1 to 5
        "your_expert_keywords_2_2":your_expert_keywords_score_2_2,
        "your_expert_keywords_2_3":your_expert_keywords_score_2_3,
        ...
        "your_expert_keywords_2_k":your_expert_keywords_score_2_k
      }
    }
  ]
}
```

##### 3.4.1.2 Example of the `domains_data.json` file for `Medical` domain

```javascript
// avt-mon-med-exp/avt_mon_med_exp/domains_data.json

{
  "domains": [
    {
      "domain":"Medical",

      "tags":{
        "MentalHealth":5,
        "PTSD":5
       },

      "phrases":{
        "Mental Health":5,
        "Mental Disorders":5,
        "Disaster Mental Health":5,
        "Disaster Research":5,
        "Potentially traumatic event":5,
        "Posttraumatic stress disorder":5
      },

      "expert_keywords":{
        "MD":5,
        "Reseacher":5,
        "PhD":5,
        "Professor":5,
        "Writer":5,
        "Journalist":5,
        "Psychologist":5,
        "Psychotherapist":5,
        "Psychiatrist":5
      }
    }
  ]
}
```

#### 3.4.2 To interact with MySQL database

```python
# avt-mon-med-exp/avt_mon_med_exp/mysql_monexp_db_config.py


# create dictionary to hold connection info to <monexp_db> database
monexp_db_config = {
    'user': '<your-user>',
    'password': '<your-password>',
    'host': '127.0.0.1',
    'raise_on_warnings': True
}
```


#### 3.4.3 To interact with your Twitter account with TwitterSearch Library need create Twitter App, and getting your application tokens

```python
# avt-mon-med-exp/avt_mon_med_exp/tw_search_experts.py

def init_tw_search_lib(self, domain_keyword):
#...
        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key='<your-CONSUMER_KEY>',
            consumer_secret='<your-CONSUMER_SECRET>',
            access_token='<your-ACCESS_TOKEN>',
            access_token_secret='<your-ACCESS_TOKEN_SECRET>'
        )

# ...
```

#### 3.4.4 To use Python Geocoder Package for getting the latitude and longitude of the expert's location from the <tw_location> field in <monexp_db> database

```python
# avt-mon-med-exp/avt_mon_med_exp/tw_search_experts.py

def tw_expert_location_geocoding(self, tw_user_location):
    # ...
        g = geocoder.bing(tw_user_location, key='<your-api_key>')
    # ...
```

#### 3.4.5 How to use Amazon Comprehend Medical operations using the Python

[Detecting medical entities using the AWS SDK for Python (Boto3)](https://docs.aws.amazon.com/comprehend-medical/latest/dev/gettingstarted-api.html#med-examples-python)


### 3.5 Run the `avtMonMedExp` application

```python
# avt-mon-med-exp/avt_mon_med_exp/avt-mon-med-exp.py

Run the main application module (`avt-mon-med-exp.py`) from the `avtMonMedExp` package work folder with the following console command:

`$ avt-mon-med-exp.py`


### 3.6 Example of the results of the first launch of the `avtMonMedExp` application

#### 3.6.1 A fragment of the output of the application results to the Console(Terminal)


---------------------------------------------------------------------
 The avtMonMedExp app began to search and analyze experts on Twitter ...
 -----------------------------------------------------------------------

 ---
 Timestamp (UTC):  2022-Oct-19 20:28:27

 ---
 Prepare data from <domains_data.json> file...

 ---
 Drop <monexp_db> database...

 ---
 Create <monexp_db> database...

 ---
 Create tables in <monexp_db> database...

 ---
 Search and analysis experts from Twitter users...

 ---
 Current processing domain:  Medical

 Queries done: 1. Tweets received: 100

 ---
@AARPIntl is Twitter user No.1 was finded base on avtMonMedExp analysis

 ---
@sober_colin is Twitter user No.2 was finded base on avtMonMedExp analysis

 ---
@winstonprep is Twitter user No.3 was finded base on avtMonMedExp analysis

 ---
@ORF_CNED is Twitter user No.4 was finded base on avtMonMedExp analysis

 ---
@abaipl is Twitter user No.5 was finded base on avtMonMedExp analysis

 ---
@YouBuyWeFly2 is Twitter user No.6 was finded base on avtMonMedExp analysis

 ---
@NamraRiaz10 is Twitter user No.7 was finded base on avtMonMedExp analysis

 ---
@Anjali_711 is Twitter user No.8 was finded base on avtMonMedExp analysis

 ---
@nancycoleITV is Twitter user No.9 was finded base on avtMonMedExp analysis

 ---
@lecondoliak is Twitter user No.10 was finded base on avtMonMedExp analysis

 ---
@MissPaulaGreen is Twitter user No.11 was finded base on avtMonMedExp analysis

 ---
@L18SUM is Twitter user No.12 was finded base on avtMonMedExp analysis

 ---
@McBrideEngage is Twitter user No.13 was finded base on avtMonMedExp analysis

 ---
@GeroNews is Twitter user No.14 was finded base on avtMonMedExp analysis

 ---
@kathrobbo3 is Twitter user No.15 was finded base on avtMonMedExp analysis

 ---
@MrKSDyck is Twitter user No.16 was finded base on avtMonMedExp analysis

 ---
@PhilZimbardo is Twitter user No.17 was finded base on avtMonMedExp analysis

 ---
@noshootings is Twitter user No.18 was finded base on avtMonMedExp analysis

 ---
@StayUpMS is Twitter user No.19 was finded base on avtMonMedExp analysis
...
---
@natasha_tracy is Twitter user No.88 was finded base on avtMonMedExp analysis

 ----------------------------------------------------------
@natasha_tracy expert description: I'm an award-winning mental health writer, acclaimed speaker, host, and author of Lost Marbles: Insights into My Life with Depression and Bipolar.

 -------------------------------------------------------------------------------
Result of using the DetectEntitiesV2 operation for <tw_user_description> analysis

 -------------------------------------------------------------------------------
Entity {'Id': 1, 'BeginOffset': 7, 'EndOffset': 41, 'Score': 0.4531750977039337, 'Text': 'award-winning mental health writer', 'Category': 'PROTECTED_HEALTH_INFORMATION', 'Type': 'PROFESSION', 'Traits': []}

 ---
Press any key to continue . . .


 ---
@natasha_tracy is expert No.1 base on avtMonMedExp and Amazon Comprehend Medical (DetectEntitiesV2 operation) analysis

 ---
Press any key to continue . . . 

@hephaistos_ai is Twitter user No.110 was finded base on avtMonMedExp analysis

 ---
@TinaMarie_80s is Twitter user No.111 was finded base on avtMonMedExp analysis

 ---
@imhrAZ is Twitter user No.112 was finded base on avtMonMedExp analysis

 ---
@TheMadDruid17 is Twitter user No.113 was finded base on avtMonMedExp analysis

 ----------------------------------------------------------
@TheMadDruid17 expert description: 18+ #Autistic #Trans #Nonbinary #ADHD #Tourettes #CPTSD. Im an #artist #pagan #tech #writer #gamer #twitchaffiliate #streamer #activist & #advocate.

 -------------------------------------------------------------------------------
Result of using the DetectEntitiesV2 operation for <tw_user_description> analysis

 -------------------------------------------------------------------------------
Entity {'Id': 1, 'BeginOffset': 33, 'EndOffset': 37, 'Score': 0.8024508953094482, 'Text': 'ADHD', 'Category': 'MEDICAL_CONDITION', 'Type': 'DX_NAME', 'Traits': []}

 ---

Press any key to continue . . . 

 ---
@TheMadDruid17 is expert No.2 base on avtMonMedExp and Amazon Comprehend Medical (DetectEntitiesV2 operation) analysis

 ---
Press any key to continue . . . 

...
 ---
Timestamp (UTC):  2022-Oct-19 21:29:30
 ---------------------------------------------------------------------
 The avtMonMedExp app successfully completed.
  ---------------------------------------------------------------------
 Elapsed time:  01:01:03
 ---------------------------------------------------------------------


