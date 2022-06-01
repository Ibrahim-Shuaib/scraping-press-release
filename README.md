# press-release

The goal was to extract data from the following four sites. Note - layout, schema are the exact same in all urls

    • https://www.constructiondive.com/press-release/
    • https://www.retaildive.com/press-release/ 
    • https://www.k12dive.com/press-release/
    • https://www.healthcaredive.com/press-release/

These are paginated lists. Get all values until end of list. 
Within each item in the list, click into the url and that’s where ALL fields to capture live.

Sample csv file, showing format to deliver: https://drive.google.com/file/d/19RDAKNoyApylaTJVn4GYghiCThQVZTc1/view?usp=sharing

# Fields to capture:

The on-page location of each of the five fields is 

    • date
        ◦ Description: The month, day, year format. There should be quotes around the value within the final csv file.
        ◦ Sample value: “April 1, 2022”
    • pr_email
        ◦ Description:
        ◦ Sample value: jbathke@burnsmcd.com
            ▪ This field value may NOT exist. It’s optional.
    • company
        ◦ Description: this represents who posted the press release.
        ◦ Sample value: AZCO
    • title
        ◦ This is the press release title at top (NOT meta title).
        ◦ Sample value: Construction Industry Veteran Earle Cianchette Named New AZCO CEO
        ◦ 
    • url
        ◦ Description: this is the url of the page
        ◦ Sample value: https://www.constructiondive.com/press-release/20220104-construction-industry-veteran-earle-cianchette-named-new-azco-ceo/
        
there is a challenge that the email field is protected - it needs to run a javascript script to decode the email.
this has been tackled by html-requests lib.
