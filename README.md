# avtMonExp project on Python 3


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
// avtMonExp/avtMonExp/domains_data.json

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

##### 3.4.1.2 Example of the `domains_data.json` file for `Wireless_Communications` domain

```javascript
// avtMonExp/avtMonExp/domains_data.json

{
  "domains": [
    {
      "domain":"Wireless_Communications",
      "tags":{
        "Wireless":5,
        "Infrared":3,
        "Bluetooth":4,
        "Wi-Fi":4,
        "ZigBee":4,
        "Cellural":5,
        "Mobile":5,
        "Satellite":4
       },
      "phrases":{
        "Wireless Networking":4,
        "Wireless Communication Networks":5,
        "Wireless Communication Systems":5
      },
      "expert_keywords":{
        "Expert":5,
        "Leader":4,
        "Engineer":4,
        "CEO":5,
        "CTO":5,
        "PhD":4,
        "Magazine":3,
        "Journalist":4,
        "Reviewer":4,
        "Analyst":5,
        "Blogger":5,
        "Reseacher":5
      }
    }
  ]
}
```

#### 3.4.2 To interact with MySQL database

```python
# avtMonExp/avtMonExp/mysql_monexp_db_config.py

# create dictionary to hold connection info to <monexp_db> database
monexp_db_config = {
    'user': '<your-user>',
    'password': '<your-password>',
    'host': '127.0.0.1',
    'charset': 'utf8mb4'
}
```


#### 3.4.3 To interact with your Twitter account with TwitterSearch Library need create Twitter App, and getting your application tokens

```python
# avtMonExp/avtMonExp/tw_search_experts.py

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

#### 3.4.4 To use python-gmaps Package for getting the latitude and longitude of the expert's location from the <tw_location> field in <monexp_db> database

```python
# avtMonExp/avtMonExp/tw_search_experts.py

def tw_expert_location_geocoding(self, tw_user_location):
    # ...
        gmaps_request = Geocoding(api_key='<your-api_key>')
    # ...
```

### 3.5 Run the `avtMonExp` application

Run the main application module (`avtmonexp.py`) from the `avtMonExp` package with the following console command:

`$ python avtmonexp.py`


### 3.6 Example of the results of the first launch of the `avtMonExp` application

#### 3.6.1 A fragment of the output of the application results to the console

```
 ---------------------------------------------------------------------
 The avtMonExp app began to search and analyze experts on Twitter ...
 ---------------------------------------------------------------------

 ---
 Timestamp (UTC):  2018-Apr-03 14:05:04

 ---
 Prepare data from <domains_data.json> file...

 ---
 Create <monexp_db> database...

 ---
 Create tables in <monexp_db> database...

 ---
 Search and analysis experts from Twitter users...

 ---
 Current processing domain:  Wireless_Communications

 Queries done: 1. Tweets received: 100

 Queries done: 2. Tweets received: 200

 Queries done: 3. Tweets received: 300

 Queries done: 4. Tweets received: 400

 Queries done: 5. Tweets received: 500

  ---
 Current time(UTC): 14:05:26
 Elapsed time:  00:00:22

 ---
 Now the avtMonExp app is suspended for 60 seconds to avoid rate-limitation by Twitter...

 ---
 Resume processing and analysis...

 Queries done: 6. Tweets received: 600

 Queries done: 7. Tweets received: 700

 Queries done: 8. Tweets received: 800

 Queries done: 9. Tweets received: 900

 Queries done: 10. Tweets received: 1000

 ---
 Current time(UTC):  14:06:33
 Elapsed time:  00:01:29

 ---
 Now the avtMonExp app is suspended for 60 seconds to avoid rate-limitation by Twitter...

  ---
 Resume processing and analysis...

 Queries done: 11. Tweets received: 1100

 Queries done: 12. Tweets received: 1200

 Queries done: 13. Tweets received: 1300

 Queries done: 14. Tweets received: 1400

 Queries done: 15. Tweets received: 1500

 ---
 Current time(UTC):  14:07:41
 Elapsed time:  00:02:37

 ---
 Now the avtMonExp app is suspended for 60 seconds to avoid rate-limitation by Twitter...
 ...
 ...
 ...
 ---
 Resume processing and analysis...

 Queries done: 46. Tweets received: 4600

 Queries done: 47. Tweets received: 4700

 Queries done: 48. Tweets received: 4800

 Queries done: 49. Tweets received: 4900

 Queries done: 50. Tweets received: 5000

 ---
 Current time(UTC):  14:53:40
 Elapsed time:  00:48:35

 ---
 Now the avtMonExp app is suspended for 60 seconds to avoid rate-limitation by Twitter...
 ...
 ...
 ...
  ---
 Resume processing and analysis...

 Queries done: 91. Tweets received: 9100

 Queries done: 92. Tweets received: 9200

 Queries done: 93. Tweets received: 9300

 Queries done: 94. Tweets received: 9400

 Queries done: 95. Tweets received: 9500

 ---
 Current time(UTC):  15:03:51
 Elapsed time:  00:58:47

 ---
 Now the avtMonExp app is suspended for 60 seconds to avoid rate-limitation by Twitter...
  ---
 Resume processing and analysis...
 ...
 ...
 ...
  ---
 Generate HTML and display experts for each domain on Google Maps in default browser...

 ---
 Copy exists <Wireless_Communications_experts.html> file to <Wireless_Communications_experts.bak> file...

 ---
 New <Wireless_Communications_experts.html> file was successfully generated...

 ---
 Open new <Wireless_Communications_experts.html> file in default browser...

 ---
 Timestamp (UTC):  2018-Apr-03 15:06:08

 ---------------------------------------------------------------------
 The avtMonExp app successfully completed.
  ---------------------------------------------------------------------
 Elapsed time:  01:01:03
 ---------------------------------------------------------------------
```

#### 3.6.2 Displaying experts for each domain on Google Maps in default browser

Results of data processing for each domain are saved in the `experts_data_viz_html` project folder. The file name corresponds to the following pattern: `domain_experts.html`. 
The `avtMonExp` app automatically opens this file in the default browser.

For example, for the `Wireless_Communications` domain, the result is as follows:
`avtMonExp/avtMonExp/experts_data_viz_html/Wireless_Communications_experts.html`

**NOTE:** If the same file already exists in the `experts_data_viz_html` folder when creating a new `*.html` file, it is copied to a file with the `*.bak` extension, and the existing `*.html` file is overwritten with a new `*.html` file with the same name.

Example of plotting expert data from the specified domain on Google Maps as heatmap in the default browser

![Plotting expert data from the the `Wireless_Communications` domain on Google Maps as heatmap in the default browser](https://software.avt.dn.ua/wp-content/uploads/2018/04/avtsoft_avtMonExp_Wireless_Communications_experts_on_GMaps_800x576.png)
