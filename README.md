# Munsell - RGB Colour Tables		
Based on Conversions Between the Munsell and sRGB Colour Systems <br/>	
by	Paul Centore © 26 April 2013		

<a href="https://www.andrewwerth.com/aboutmunsell/"><img src="https://www.andrewwerth.com/wp-content/uploads/2013/08/munsellicon.jpg"><br/>Virtual Munsell Color Wheel<br/> by Andrew Werth © 2023<br/>All rights reserved.</a>

### Related references  
http://www.andrewwerth.com/color/
https://www.andrewwerth.com/aboutmunsell
http://www.huevaluechroma.com/011.php

## The Munsel Color System

<img src="https://munsell.com/wp-content/uploads/2015/08/munsell-color-tree-blue-green.jpg" width=33% height=33%>

The Munsell Color system, is based on rigorous measurements of human subjects' visual responses to color, putting it on a firm experimental scientific basis. Because of this basis in human visual perception, Munsell's system has outlasted its contemporary color models, is still in wide use today.  (see Wikipedia/Munsell_color_system)

## The 3-D Color Space
Munsell's Color Conversion List describes the mapping between the RGB Color Space and the Munsell Color Space of Hue, Value and Chroma. It was created using experimental human observations. There is no simple linear equation for associating Munsell Color Keys with RGB color values. These associations require table lookups.  

## The Munsell Color Tree
The Munsell Color Space can be visualized and explored as a set of Hue Pages all oriented perpendicular to a horizontal base, all connected to a vertical shaft at the center of the flat base. Each page of this Tree is rotated some number of degrees about the vertical axis of the shaft. The color Red is typically set to be 0 degress. Then going counter-clockwise, the next Color or HuePrefix, Yellow, is set at 72 degrees. The other Hue Pages have increasing degree headings up to Red-Purple, which has a setting of 324 degrees.  The next hue then comes back to Red at 360 or 0 degrees.

One explanation of <a href="https://munsell.com/color-blog/color-tree/#:~:text=The%20trunk%20of%20the%20tree,goes%20from%20light%20to%20dark.">the Munsell Color tree</a> (currently available for purchase at <a href="https://www.amazon.com/s?k=munsell+color+tree&crid=3KCB09105J62H&sprefix=munsell+color+tree%2Caps%2C153&ref=nb_sb_noss_1">Amazon.com for $424</a>) uses five primary Hues and five intermediate Hues making ten `color branches`. The Munsell-to-RGB-Tables spreadsheet splits the color space into 10 primary HuePrefixes each with 4 intermediate Hues.

## The Munsell-to-RGB-Tables macro-enabled spreadsheet 
The `Munsell-to-RGB-Tables` are described in an Excel spreadsheet with macros enabled named `Munsell-to-RGB-Tables.xlsm`. When opening this file in Excel be sure not to ignore the macros. The macros are critical to the functionality of some of the sheets. 

The sheets of this spreadsheet are as follows:  

* Intro - gives credit to the creators of this file.
* Setup - describes 10 basic Colors or HuePrefixes each with their 4 intermediate Hues.
* HuePages - describes how HuePrefix and intermediate Hues define each HuePage.
* Conversion Lists - describes the mapping between Munsell Keys and RGB Color values.
* Grey lists - shows the 11 grey values that are defined along the vertical shaft mentioned above from black at the bottom to white at the top.
* Value-Chroma - is a macro-driven page that shows Values and Chroma for a given HuePage defined by its HuePrefix and Hue using the dropdowns at the top left. 
* HuePrefix-Chroma - is a macro-driven page that shows the 10 HuePrefix pages for a selected Value and Hue using the dropdowns at the top left.
* Hue-Chroma - this macro-driven page shows Hue and Chroma for a selected HuePrefix and Value using the dropdowns at the top left.

## Macro-driven Sheets
Note that macro-driven sheets are oriented differently in the Munsell Color Tree. Value is oriented vertically along the y-axis with black at the bottom and white at the top. Chroma is shown horizontally on each page on the x-axis with zero chroma as gray on the left and maximum chroma on the right.

Note that the Hue dropdown on the Value-Chroma page currently not working for choices 5.0 and 10.0.

## Munsell vs RGB color gamut
Note that the shape of the Value and Chroma combinations on the HuePrefix/Hue pages do not fill the entire page. This illustrates the non-linear nature of the HVC mapping to RGB. The color gamut of the Munsell Color space does not match the color gamut of the RGB color space.

## Muncell Dimensions
Munsell Tree partitioning is:  
* 10 Colors or HuePrefixes  
* 4 intermediate Hue-Pages per HuePrefix = 40 Hue-Pages
* 9 Value-Rows per Hue-Page  
* ~8 Chroma-Columns per Value-Row \(approx average\)  
with a total of 2,734 Color Chips 

## The Munsell Color Chips  
Munsell Color Tree models are available at many retail outlets, including Amazon.com. These models use Pantone paint chips, which explains the hight cost.

Each Color Chip in the `Conversion Lists` sheet has a unique RGB Color Value Munsell Color Key. The Munsell Color Key encoding format is:    
```
    (<Hue><HuePrefix>)-<Value>-<Chroma>
```

For example, Munsell Key `10.0RP-3-12` decodes to   
    HuePrefix = `RP`   
    Hue = `10.0`  
    Value = `3`  
    Chroma = `12`  

So, in 3-D Munsell space this chip has location  
HuePage=`10.0RP` (or Page#=`40`), Row=`3`, Column=`12`. 

This example Munsell Color Key is at row `2689`, column `F` in the `Conversion List` table. The corrsponding RGB Color Value is next to it at column `G` is `149,0,69`.

## Conclusion  
Given this interpretation of the Munsell Color Space, the `Munsell-to-RGB-Tables` spreadsheet should be sufficient for building a responsive single page web application that can be used to explore this unique model of color based on human visual perception.


