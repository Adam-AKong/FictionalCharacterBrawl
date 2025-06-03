## Fake Data Modeling
# Code

```uv run simulate.py```

The Code for each section is under src/simulate

# Estimated Total RowsRows
This is taken from simulate.py

user_total = 200,000
franchise_total = 1,000
character_total = 150,000 = 50,000 * 3 average franchises per character
review_total = 400,000 = 200,000 * 2 (franchise and character reviews)
battle_total = 250,000 = 50,000 * 5 (average votes per battle)
Total estimated rows ~ 1,000,000

I believe the database will scale like this where the majority is focused upon the amount of Users itself. Frachises probably won't get that big as there are only so many popular franchises out there, however I included the possibility of people creating less popular known franchises or even their own custom ones. With 200,000 users, its possible for franchises themself to reach 1,000. Furthermore, I don't expect every user to be creating characters as the vast majority I believe will just use the database to scroll and look at other comments. However, with 150,000 users, some might create multiple while others making none, which is why I estimated 50,000 total characters being made. This is quite a lot even still as that means its an average of 50 characters per franchise. However, duplicate characters can exist as users have the freedom to determine the stats of the characters. Since you can assign multiple franchises, I imagine some users would want to create characters that are involved in multiple franchises due to parady or their own custom franchise/characters made with friends. I estimated that on average a user would want to make 2 reviews each. The simulated data does an even split of characters/franchises, which I don't expect to happen, but for the sake of testing the efficiency of endpoints I decided to implement that. Once again, not every user will create reviews, but the more active ones could potentially create multiple upwards to dozens if not hundreds, while the vast majority will stay silent and just browse the content. Lastly the battles are a secondary source of our project with the main focus being the database of characters franchises. With that being said, I estimated the amount of battles to be less than the reviews as most people probably won't actually care too much about some silly online battle system with unregulated character stats. However, since they are so easy to create and vote upon, I imagine there will be a decent following from active individuals allowing for a solid on average 1 battle for every 4 users. Voting I created to be 0-10 in the simulated data, witt it being 5 on average, making it 250,000 total rows.