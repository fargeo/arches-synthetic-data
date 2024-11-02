# Welcome to the Arches Project!

To create resources for the bulk loader run you'll first need to install the package:

```
python manage.py packages -o load_package -a synthetic_data -db -y -dev
```

Then you can start creating resources in single csv format:
```
python manage.py resource_generator -d ~/Desktop/synth-data.csv -r 25000
```

`-d --dest` the output file 
`-r --resources` number of resources you wish to create

