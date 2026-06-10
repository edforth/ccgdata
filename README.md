# Purpose
The goal of the TCG Data project is to provide a public data set concerning card and game details for dead collectible card games and trading card games to support software development, discussion, and interest regarding these games.

# Scope
This project is focused on documenting dead TCGs.  

A game is considered a "TCG" for this project if players are expected to assemble their own beginning game items out of their own collections before beginning a game.  "Deck Building" games such as Dominion, or Ascension that include all components for all players and expect the players to assemble their decks out of this shared pool during the course of the game are out of scope for this project. "LCGs" like Doomtown: Reloaded or Android: Netrunner that are sold as full sets, but still require expect players to assemble their own sets of beginning components are in scope for this project.

A game does not need to be limited to cards, such as Dice Masters, nor does it need to use cards at all, such as Dragon Dice, to be in scope for this project. 

A TCG is considered "dead" when it has been cancelled by it's designers and is not expected to receive new additions.  We may choose to include a game that is later revived, such as Overpower, but we will not cover the new publisher's additions.  This chose is primarily due to the additional resources needed to provide ongoing coverage to a "live" game.

# Sources
Any item data used in the TCG Data project must be from an appropriate source.

The ranking of sources from most preferred to least preferred is
* A physical copy of an actual game item in the possession of a trusted TCG Data Project contributor
* A photograph of a physical game item
* An official document from the publisher of the game
* A document from a trusted third party source

# Definitions of Done
**Item Complete**: A Game or Set is labeled as Item Complete when we believe we have an entry for every item in that game or set in our dataset.

**Data Complete**: A Game or Set is labeled as Data Complete when we have included all attribute data for each item in that game or set in our dataset.

**Image Complete**: A Game or Set is labeled as Image Complete when we have created, or been donated high quality images covering all relevant attributes of each item in the game or set.

# Style Guide
Our goal is to accurately document TCGs as they were designed and released. Whereever possible, the style and errors present in a release item should be preserved.  If their is a need to include corrections or errata, they should be included in addition to the original, published form. 

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
        - If they only variances for the item are already captured in other attributes, e.g. "language" or "finish", use the minimum combination of these attributes necessary to identify the variances.
        - If there is an existing disambiguator in common use among the game's community already, we should adopt it, as long as it meets the above requirements
        - Shorter values are preferred over longer values when the above requirements are met as this value will be used in the creation of other values
- source - a string indicating the source of the data for this item.   Acceptable values are ("item", "photo", "first-party-document", "third-party-document")
- images - a JSON list of filenames without extensions that can be used to uniquely identify images for the item.
- attributes - a JSON object describing all relevant attributes of the game item.

# Supported Data Formats
Currently, we intend to maintain per-game CSVs with all item data. These CSVs will be regenerated as needed from our project database.  We also intend to move our database files into github when we are able.

Our desire is to provide a robust set of data formats to support other projects.  If you have a project that would benefit from different data formats, please reach out or create an issue. 

# Current Game Statuses
## Rage - Data Complete - Images: 1099/1294 (85%)
- Limited Edition - Data Complete - Images: 307/321 (96%)
- Unlimited Edition - Data Complete - Images: 319/321 (99%)
- The Umbra - Data Complete - Image Complete: 95/95 (100%)
- The Wyrm - Data Complete - Images: 143/185 (77%)
- The War of the Amazon - Data Complete - Images: 75/140 (54%)
- Legacy of the Tribes - Data Complete - Images: 159/215 (74%)

https://archive.org/details/rage-ccg_hd-scans

## The Crow - Data Complete: 123/123 - Images: 26/123 (21%)
- Limited Edition - Data Complete 122/122 - Images: 26/122 (21%)
- Promo - Data Complete 1/1 - Images: 0/1 (0%)

https://archive.org/details/the-crow_card-scans

## On the Edge - 
- Limited Edition - 269/269 Variants unknown
- Unlimited Edition - 269/269 Variants unknown
- Standard Edition - Item Complete: 283/283 - Images: 
- The Cut-Ups Project - Item Complete: 133/133
- Shadows - Item Complete: 121/121
- Arcana - Item Complete: 169/169
- Specials - Item Complete: 24/24

https://archive.org/details/on-the-edge-ccg-hd-scans
