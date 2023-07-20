Due to potential computation time limitations, we are following the below number of perturbations to create datasets : 
##For gender bias
- Total of 150 perturbations for each template
- Create 50 perturbations for male, female and unisex names
- Select 50 names randomly from top 1000 names for male and female (removing 97 names which are unisex names, so 903 top binary names)
- Select top 50 names for unisex from https://github.com/fivethirtyeight/data/blob/master/unisex-names/unisex_names_table.csv

##For racial bias
- Total 200 perturbations for each template
- Create 50 perturbations for white, black, asian and hispanic names based on US census data
- Select 50 names randomly from top 300 names for white, black, asian and hispanic names
