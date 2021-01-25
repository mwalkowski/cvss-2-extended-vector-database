# CVSS 2.0 extended vector database

## Description
The repository contains data that may be useful in the process of creating machine learning algorithms to convert from [CVSS Base Scoring 2.0](https://www.first.org/cvss/v2/guide) to
[CVSS Base Scoring 3.x](https://www.first.org/cvss/specification-document).

The data was obtained using the open source [VMC](https://github.com/DSecureMe/vmc) tool, which provides a database containing vulnerabilities
and weaknesses from publicly monitored sources. The [VMC](https://github.com/DSecureMe/vmc) tool also provides Python API,
thanks to which the [input_data](./input_data/cvss_2_3.csv) dictionary containing 73,179 items was prepared using the [get_data.py](./get_data.py) script.
By the [NLTK](https://www.nltk.org/) library removed all stop words and stemming was used.
From the 3,458,874 base words obtained, 50 base words were selected that were most frequently repeated in the vulnerability descriptions [Table 1](https://github.com/mwalkowski/cvss-2-extended-vector-database/new/main?readme=1#table-1-top-50-words-used-in-the-vulnerability-descriptions)

#### Table 1. Top 50 words used in the vulnerability descriptions.
|     Word|Occurrence|       Word |Occurrence|
|---------|---------:|------------|---------:|
|attack   |     7 651|occur       |    25 796|
|vulner   |    58 552|intend      |    25 060|
|use      |    57 004|file        |    24 946|
|softwar  |    55 083|via         |    24 889|
|allow    |    54 956|version     |    23 275|
|memori   |    51 871|command     |    21 736|
|data     |    47 988|read        |    21 350|
|input    |    46 503|affect      |    21 269|
|execut   |    41 279|remot       |    21 196|
|access   |    40 890|oper        |    21 113|
|buffer   |    40 414|incorrectli |    21 081|
|user     |    39 215|program     |    20 928|
|inform   |    37 613|privileg    |    20 572|
|valid    |    37 535|perform     |    18 774|
|code     |    36 366|applic      |    18 223|
|locat    |    35 926|craft       |    18 082|
|may      |    34 831|pointer     |    17 641|
|could    |    30 801|lead        |    17 119|
|caus     |    30 301|issu        |    17 000|
|neutral  |    28 697|outsid      |    16 978|
|result   |    28 646|web         |    16 736|
|control  |    27 695|write       |    16 625|
|arbitrari|    27 296|compon      |    16 519|
|resourc  |    27 092|exploit     |    16 034|
|system   |    26 348|actor       |    15 934|

Using the [main.py](./main.py) script, the [output_data](./output_data/data_word_50.csv) file was created
containg data in the form of training vectors:
```
X 1:57
Y 58:66
```


## Files
* [get_data.py](./get_data.py) - script that retrieves data from the [VMC](https://github.com/DSecureMe/vmc) tool.
* [main.py](./main.py) - script that converts the input data into the training vectors.
* [input_data](./input_data/cvss_2_3.csv) - data received with the script [get_data.py](./get_data.py)
  from the [VMC](https://github.com/DSecureMe/vmc) tool, contains a description of the vulnerability and the associated weakness,
  a CVSS Base 2.0 vector in numerical form, and a CVSS Base 3.x vector as the numbers corresponding to their class.
* [output_data](./output_data/data_word_50.csv) - data obtained using the script [main.py](./main.py)
   described in the [Description](https://github.com/mwalkowski/cvss-2-extended-vector-database/new/main?readme=1#table-1-top-50-words-used-in-the-vulnerability-descriptions) section.


## How to generate data
The shared files allow to conduct the individual research by anyone interested, regarding conversion
CVSS Base 2.0 on CVSS Base 3.x. In order to generate new data, use Python 3.9 and execute the following commands:
```
virtualenv env
source env/bin/activate
pip3 install -r requiements.txt
python3 main.py
```
Sample program output:
```
Loading data...
Data loaded, creating words list...
All used words 3458874 counting frequency...
Selecting top 50 used words...
Words selected, sorting alphabetically..
Preparing output...
Output data count 73179
Output saved
X 1:57
All columns 66
```

## Authors
Michał Walkowski <michal.walkowski at pwr.edu.pl>  
Maciej Nowak <maciej.nowak at pwr.edu.pl>  
Sławomir Sujecki <slawomir.sujecki at pwr.edu.pl>
