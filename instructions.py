create a python3 app that takes no command line arguments

hard-code the relative path of a local 
Excel Spreadsheet file named 
"Munsell-to-RGB-Tables.xlsm"

take the "HuePages" sheet of the Excel file
to create a pandas dataframe named HuePages 
with 40 rows, each with columnNames created by combining 
the first and second rows of each column:
    page_Color, 
    page_HuePrefix, 
    page_Hue, 
    page_HueName, 
    page_number, 
    page_degrees, 
    page_imageFile

take the "Conversion Lists" sheet of the Excel file 
to create a pandas dataframe named ConversionList 
with columnNames created by combining the first and second
rows of each column:
    page_HuePrefix
    page_Hue
    page_HueName
    page_number

use the common columns of both pages to join
the two dataframe to add the page_Color,
page_number, page_degrees, and page_imageFile
columns to the ConversionList dataframe.


Revise the columnNames as needed to give the
expected results.

Use the remaining ConversionList columns:
    row_Value
    column_Chroma
    chip_ColorKey
    chip_RGB
    chip_number
To create a 2-D array of ColorChip objects to
for each HuePage.

This 2-D array has 9 rows corresponding to the 
9 different row_Values for each HuePage and 
10 columns corresponding to the column_Chroma values
for each row_Value.

Each row/column pair has a ColorChip with 3 properties:
    chip_colorKey
    chip_RGB
    chip_number
All pulled from the 3 chip columns of the ConversionList table.

Most row_Values will have less than all 10 column_Chroma
of chip data available in the ConversionList table. 
Set the three ColorChip properties of these chips to null.

For each HuePage create a 2D image that renders the 
9 x 10 matrix of ColorChips. Each rendered as
a square of size 70x70 pixels with background color
taken from that ColorChip's chip_RGB value. 

Separate all rows and columns of ColorChips with 
10 pixel gap. 

Give each ColorChip a 1 pixel border
of white or black, depending on which color
has the highest contrast against the chip's
background color.

Set the background color of each HuePage image 
to transparent and save each HuePage image as a
PNG file using its page_imageFile property
and save it to a local folder named 
"HuePages_rendered".

Make sure that comments are wrapped to fit
within a maximum width of 80 characters.