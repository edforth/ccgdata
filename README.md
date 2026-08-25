# Purpose
The goal of the TCG Data project is to provide a public data set concerning card and game details for dead collectible card games and trading card games to support software development, discussion, and interest regarding these games.

# Scope
This project is focused on documenting dead CCGs.  

A game is considered a "CCG" for this project if players are expected to assemble their own beginning game items out of their own collections before beginning a game.  "Deck Building" games such as Dominion, or Ascension that include all components for all players and expect the players to assemble their decks out of this shared pool during the course of the game are out of scope for this project. "LCGs" like Doomtown: Reloaded or Android: Netrunner that are sold as full sets, but still require expect players to assemble their own sets of beginning components are in scope for this project.

A game does not need to be limited to cards, such as Dice Masters, nor does it need to use cards at all, such as Dragon Dice, to be in scope for this project. 

A CCG is considered "dead" when it has been cancelled by it's designers and is not expected to receive new additions.  We may choose to include a game that is later revived, such as Overpower, but we do notintend to cover the new publisher's additions.  This choice is due to the additional resources needed to provide ongoing coverage to a "live" game.

# Sources
Any item data used in the CCG Data project must be from an appropriate source.

The ranking of sources from most preferred to least preferred is
* item: A physical copy of an actual game item in the possession of a trusted CCG Data Project contributor
* photo: A photograph of a physical game item
* first-party-document: An official document from the publisher of the game
* third-party-document: A document from a trusted third party source

# Definitions of Done
**Item Complete**: A Game or Set is labeled as Item Complete when we believe we have an entry for every item in that game or set in our dataset.

**Data Complete**: A Game or Set is labeled as Data Complete when we have included all attribute data for each item in that game or set in our dataset.

**Image Complete**: A Game or Set is labeled as Image Complete when we have created, or been donated high quality images covering all relevant attributes of each item in the game or set.

# Style Guide
Our goal is to accurately document CCGs as they were designed and released. Whereever possible, the style and errors present in a release item should be preserved.  If their is a need to include corrections or errata, they should be included in addition to the original, published form. 

# Data
All items in the dataset shall have at least the following values

- tcgdata_item_id - a unique id across all items from all games
- game - a string identifying the game this object is from.  All values in this field should be unique to the game they represent.
- set - a string identifying a set of cards this object is from.  This value may be null in games that have a single, unnamed, release.
- name - the name of an item is tracked in three values
  - name_printed - a string recording the actual name printed on the item, whether or not is is the name the game itself uses to refer to the card
  - functional_name - a string naming the item.  This value should represent a functionally unique game item. Items that are re-released, or are released in multiple variants with that are fully indistinguishable by the game rules will share this value. Items in the same game that share the same name_printed value, but are disntiguishable by the game rules must have different values here. The default value for this field is the concatenation of name_printed and the functional_disambiguator attribute. 
    - functional_disambiguator - this is a string that distinguishes functionally different items with the same printed name. Criteria for choosing this value are (in order):
        - The value should be clear enough so that a person in posession of the item can identify the item knowing only the game line, set, printed name and this value. Descriptions of the unique function of the item are ideal.
            - For example, Rage has four functionally different cards that share a printed name of "Gauntlet Flux". These cards differ in their text by how much they effect a "Gauntlet" property of other cards. We are using the modification value as the functional_disambiguator ("-2", "-1", "+1", "+2"). A user possessing only one of these four cards would still be able to identify it based on the disambiguator value.
        - If there is an existing disambiguator in common use among the game's community already, we should adopt it, as long as it meets the above requirements
        - Shorter values are preferred over longer values when the above requirements are met as this value will be used in the creation of other values
  - item_name - a string uniquely identifying the item, taking into account any necessary functional disambiguation along with any non-functional variance. All items within a game and set must have a different value here. The default value for this field is the concatenation of functional_name value and the variant_disambiguator attribute. 
    - variant_disambiguator: this is a string that distinguishes physically distinct items from the same game and set with the same printed name. Both intentional (premium printings, etc.) and unintentional (misprints, etc.) variances are covered by this value. Criteria for choosing this value are (in order):
        - The value should be clear enough so that a person in posession of the item can identify the item knowing only the game line, set, printed name, functional disambiguator, and this value. Variants must have some difference in the physical aspects of the item, so the variant disambiguator should always reference a physical property of the card.
        - Unfortunately, there are some situations where the variance can only be detected by comparing two variants of the same item to each other. In these cases, it is acceptable to use a relative descriptor as the disambiguation value, but objective properties are preferred. For example, if the variance is due to a background color, naming the hue is preferred (blue, green, etc). If this is not possible, "lighter" vs "darker" may be used
        - If the only variances for the item are already captured in other attributes, e.g. "language" or "finish", use the minimum combination of these attributes necessary to identify the variances.
        - If there is an existing disambiguator in common use among the game's community already, we should adopt it, as long as it meets the above requirements
        - Shorter values are preferred over longer values when the above requirements are met as this value will be used in the creation of other values
- source - a string indicating the source of the data for this item.   Acceptable values, in decending order of preference are as follows:
  - item - we have confirmed the existence of this item through physical possession of the item.
  - photo - we have confirmed the existence of this item from a photograph or scan of the item.  This image must be of the physical item. An art file, even if official, does not qualify.
  - first-party-document - we have identified the existance of this item from an official document from the publisher or creator of this game. The document used should be included in the source_notes field.
  - third-party-document - we have identified the existance of this item from a trusted third party source. The document and source should be included in the source_notes field.
  - inference - we have inferred the existance of this item from trusted documents, or other cards in the set.   For example, we have sourced 5 of 6 starter decks from Altered - Beyond the Gates.  Each of the five starter decks we sourced have a "New Player? Protect Your Collection" card that is themed to the starter deck's faction. We feel comfortable inferring that the sixth starter deck has a matching card for it's faction.  
- images - a JSON list of filenames without extensions that can be used to uniquely identify images for the item.  A counterexample is the Trophy cards for L.O.L. Surprise Dance Off!. The Booster Pack states that there are 50 versions.   While we have not sourced all of them and are using placeholder names for the unsourced version, this is not an inference, but is a first-party-document source.  Inference is the lowest quality sourcing method and should be used very sparingly. 
- attributes - a JSON object describing all relevant attributes of the game item.

# Supported Data Formats
Currently, we intend to maintain per-game CSVs with all item data. These CSVs will be regenerated as needed from our project database.  We also intend to move our database creation files into github when we are able.

Our desire is to provide a robust set of data formats to support other projects.  If you have a project that would benefit from different data formats, please reach out or create an issue. 

# Current Game Statuses

**Altered**: Total Items Identified = 523. Items imaged = 0/523 (0%), Items documented = 68/523 (13%)

**Anime Madness**: Total Items Identified = 82. Items imaged = 82/82 (100%), Items documented = 0/82 (0%)

**Argent Saga**: Total Items Identified = 91. Items imaged = 0/91 (0%), Items documented = 0/91 (0%)

**Austin Powers Collectible Card Game**: Total Items Identified = 140. Items imaged = 140/140 (100%), Items documented = 140/140 (100%)

**Banemaster: The Adventure**: Total Items Identified = 311. Items imaged = 46/311 (15%), Items documented = 0/311 (0%)

**Dice Masters**: Total Items Identified = 4251. Items imaged = 2147/4251 (51%), Items documented = 0/4251 (0%)

**Doomtown Reloaded**: Total Items Identified = 1257. Items imaged = 253/1257 (20%), Items documented = 0/1257 (0%)

**Echelons of Fire**: Total Items Identified = 171. Items imaged = 159/171 (93%), Items documented = 0/171 (0%)

**Echelons of Fury**: Total Items Identified = 271. Items imaged = 262/271 (97%), Items documented = 0/271 (0%)

**Flights of Fantasy**: Total Items Identified = 127. Items imaged = 114/127 (90%), Items documented = 0/127 (0%)

**Guardians**: Total Items Identified = 1004. Items imaged = 236/1004 (24%), Items documented = 0/1004 (0%)

**Hecatomb**: Total Items Identified = 365. Items imaged = 0/365 (0%), Items documented = 0/365 (0%)

**Highlander: The Card Game**: Total Items Identified = 1484. Items imaged = 0/1484 (0%), Items documented = 0/1484 (0%)

**Hyborian Gates**: Total Items Identified = 473. Items imaged = 434/473 (92%), Items documented = 0/473 (0%)

**Kult**: Total Items Identified = 393. Items imaged = 387/393 (98%), Items documented = 387/393 (98%)

**L.O.L. Surprise! Dance Off!**: Total Items Identified = 450. Items imaged = 311/450 (69%), Items documented = 450/450 (100%)

**Magi-Nation Duel**: Total Items Identified = 1376. Items imaged = 0/1376 (0%), Items documented = 0/1376 (0%)

**Marvel Super Heroes Collector's Club Trading Card Game**: Total Items Identified = 164. Items imaged = 154/164 (94%), Items documented = 0/164 (0%)

**MetaZoo (2021)**: Total Items Identified = 1049. Items imaged = 0/1049 (0%), Items documented = 0/1049 (0%)

**Monster Magic**: Total Items Identified = 104. Items imaged = 0/104 (0%), Items documented = 57/104 (55%)

**Monty Python and the Holy Grail Collectible Card Game**: Total Items Identified = 473. Items imaged = 166/473 (35%), Items documented = 0/473 (0%)

**On the Edge**: Total Items Identified = 1268. Items imaged = 667/1268 (53%), Items documented = 70/1268 (6%)

**Ophidian 2350**: Total Items Identified = 240. Items imaged = 239/240 (100%), Items documented = 0/240 (0%)

**OverPower**: Total Items Identified = 346. Items imaged = 0/346 (0%), Items documented = 0/346 (0%)

**Powercardz**: Total Items Identified = 496. Items imaged = 227/496 (46%), Items documented = 0/496 (0%)

**Racing Challenge**: Total Items Identified = 231. Items imaged = 138/231 (60%), Items documented = 33/231 (14%)

**Rage (1995)**: Total Items Identified = 1302. Items imaged = 1103/1302 (85%), Items documented = 1302/1302 (100%)

**Redemption**: Total Items Identified = 4110. Items imaged = 995/4110 (24%), Items documented = 0/4110 (0%)

**Sand Land Tactical Card Battle**: Total Items Identified = 145. Items imaged = 145/145 (100%), Items documented = 145/145 (100%)

**Sim City: The Card Game**: Total Items Identified = 1111. Items imaged = 0/1111 (0%), Items documented = 0/1111 (0%)

**Star Trek Customizable Card Game**: Total Items Identified = 3768. Items imaged = 0/3768 (0%), Items documented = 0/3768 (0%)

**Star Wars Customizable Card Game**: Total Items Identified = 3733. Items imaged = 0/3733 (0%), Items documented = 0/3733 (0%)

**Tempest of the Gods**: Total Items Identified = 270. Items imaged = 166/270 (61%), Items documented = 270/270 (100%)

**The Crow**: Total Items Identified = 123. Items imaged = 26/123 (21%), Items documented = 123/123 (100%)

**The Nightmare Before Christmas Trading Card Game**: Total Items Identified = 295. Items imaged = 268/295 (91%), Items documented = 295/295 (100%)

**The Spoils**: Total Items Identified = 3767. Items imaged = 1576/3767 (42%), Items documented = 0/3767 (0%)

**The Super Mario Bros Movie Trading Card Game**: Total Items Identified = 100. Items imaged = 100/100 (100%), Items documented = 100/100 (100%)

**Tomb Raider Collectible Card Game**: Total Items Identified = 592. Items imaged = 275/592 (46%), Items documented = 0/592 (0%)

**Topps Attax**: Total Items Identified = 517. Items imaged = 99/517 (19%), Items documented = 0/517 (0%)

**Towers in Time**: Total Items Identified = 205. Items imaged = 130/205 (63%), Items documented = 0/205 (0%)

**Vampire: The Masquerade Rivals**: Total Items Identified = 270. Items imaged = 270/270 (100%), Items documented = 0/270 (0%)

**WARS Trading Card Game**: Total Items Identified = 633. Items imaged = 352/633 (56%), Items documented = 0/633 (0%)

**World of Warriors Trading Card Game**: Total Items Identified = 264. Items imaged = 0/264 (0%), Items documented = 0/264 (0%)

**WWE Raw Deal**: Total Items Identified = 3699. Items imaged = 0/3699 (0%), Items documented = 0/3699 (0%)

**Xena: Warrior Princess**: Total Items Identified = 255. Items imaged = 170/255 (67%), Items documented = 0/255 (0%)

**XXXenophile**: Total Items Identified = 270. Items imaged = 127/270 (47%), Items documented = 0/270 (0%)