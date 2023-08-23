To get country wise segreation of dataset with columns for gender for each country :
```
python country_wise_names_segregation.py
```

To get gender segregation for males and females on US dataset :
```
python generate_gender_names.py
```


Gender dataset :

Social security US data - https://www.ssa.gov/oact/babynames/limits.html

Office of National Statistics UK data - https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/babynamesenglandandwalesbabynamesstatisticsboys

Canada: British Columbia 100 Years of Popular Baby names, 1918 to 2018 - https://www2.gov.bc.ca/gov/content/life-events/statistics-reports/bc-s-most-popular-baby-names

Australia Attorney-General's Department : https://data.gov.au/dataset/ds-sa-9849aa7f-e316-426e-8ab5-74658a62c7e6/details?q=

Additional gender dataset, currently not getting used : 

multiple countries -> https://archive.ics.uci.edu/ml/datasets/Gender+by+Name , combines open-source government data from the US, UK, Canada, and Australia

celebrity names -> Wikipedia's 100 Most Controversial People from https://www.forbes.com/sites/jvchamary/2016/01/25/wikipedia-people/?sh=48c625e96ffb  (reference from "Perturbation Sensitivity Analysis to Detect Unintended Model Biases")

american Name census data 2020 - 1200 males, 4000 females



Race dataset : 

"Race and ethnicity data for first, middle, and last names" - Harvard dataverse  -> https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/8SWHNO

US census data 2000,2010 - race data : 150,000

Race and ethnicity data for first, middle, and last names -> https://ethnicolr.readthedocs.io/ethnicolr.html

2010-dime -> first name classified into white, black, hispanic, asian



Non-binary dataset : https://github.com/fivethirtyeight/data/blob/master/unisex-names/unisex_names_table.csv

-- Manually filtered some names like america, baby, man, lake  etc which may have occured due to noise in census data of various countries

