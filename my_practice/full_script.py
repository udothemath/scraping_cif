# -*- coding: utf-8 -*- set the coding here as the input file contains non-ascii characters
#import modules
from mifkit import mif
from mifkit.objects import * #using import * imports all possible MIF objects
import csv

#open and parse data file
with open("input_table.csv", "rU") as f: #this opens our data file ‘input_table.csv’ in universal read mode
	reader = csv.reader(f) #parse the data using the csv module
    next(reader) #skip row one
	next(reader) #skip row two

	#create list to store data and loop through CSV file
	samples = []
	for row in reader:
		#store the reference information
		reference = Reference()
		reference.doi = row[4] #row[4] references the fifth column of the current row and the string from this cell will be stored in the doi field

		#store the material information
		material = Material()
		material.chemical_formula = row[1] #row[1] references the second column of the current row

		structure = Value()
		structure.name = "Structure"
		structure.scalar = row[0] #the structure from the first column is stored as a scalar

		crystallinity = Value()
		crystallinity.name = "Crystallinity"
		crystallinity.scalar = "Single Crystal" #This is the same for every row and is only provided in the heading so it can be hard coded

		crystal_system = Value()
		crystal_system.name = "Crystal System"
		crystal_system.scalar = "Cubic" #This is the same for every row and is only provided in the heading so it can be hard coded

		material.condition = [structure, crystallinity, crystal_system] #store a list of value objects

		#store the measurement information
		temperature = Value()
		temperature.name = "Temperature"
		temperature.scalar = "Standard" #The header states that the measurements were taken at standard conditions so this can be hard coded for each row

		pressure = Value()
		pressure.name = "Pressure"
		pressure.scalar = "Standard" #The header states that the measurements were taken at standard conditions so this can be hard coded for each row

		bulk_modulus = Value()
		bulk_modulus.name = "Bulk Modulus K$_0$" #Citrination uses LaTeX notation to represent symbols, superscripts and subscripts
		bulk_modulus.scalar = row[2] #bulk modulus is given in the third column of each row
		bulk_modulus.units = "GPa" #units are given in the heading and can be hard coded

		shear_modulus = Value()
		shear_modulus.name = "Shear Modulus G$_0$" #Citrination uses LaTeX notation to represent symbols, superscripts and subscripts
		shear_modulus.scalar = row[3] #shear modulus is given in the fourth column of each row
		shear_modulus.units = "GPa" #units are given in the heading and can be hard coded

		bulk_modulus_measurement = Measurement()
		bulk_modulus_measurement.property = bulk_modulus
		bulk_modulus_measurement.condition = [temperature, pressure]

		shear_modulus_measurement = Measurement()
		shear_modulus_measurement.property = shear_modulus
		shear_modulus_measurement.condition = [temperature, pressure]

		shear_modulus_measurement.data_type = "Experimental"
		bulk_modulus_measurement.data_type = "Experimental"

		#create a sample
		sample = Sample()
		sample.reference = reference
		sample.material = material
		sample.measurement = [bulk_modulus_measurement, shear_modulus_measurement]

		#store the sample in the samples list
		samples.append(sample)

	#dump the samples list to a JSON file
	with open("output.json", "w") as output_file: #create an output file
		mif.dump(samples, output_file, indent=4) #dump the sample list to JSON and include an indent of 4 so that the file can be reviewed more easily
