# Prompt pairs

The pairs each model generated for [Experiment 1.1](../README.md), one table per area. Each row is one topic, numbered in the order of the topics in [generation.json](generation.json). All pairs are in [prompt_pairs.jsonl](prompt_pairs.jsonl), labeled by model, category, area, and topic.

## Food and drink

### Certain

**Pair 1:** Pineapple on pizza, yes or no?

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | A travesty vs. A game-changer | An abomination vs. Brilliant | Loves it vs. "On the other hand, I cannot stand it." |
| 2 | New York vs. Neapolitan | New York vs. Chicago deep dish | Neapolitan vs. "That sounds ridiculous": deep dough with extra toppings |
| 3 | Pepsi vs. Coke | Coke vs. Pepsi | Pepsi vs. "Pepsi has got nowhere going": Coke |
| 4 | Sour cream and onion vs. Smoky BBQ | Barbecue vs. Sour cream and onion | Hates sour cream and chives vs. Loves sour cream and chives |
| 5 | Five Guys vs. In-N-Out | McDonald's Big Mac vs. Burger King Whopper | Big Mac vs. Whopper |
| 6 | Five Guys vs. Chick-fil-A waffle fries | McDonald's vs. Wendy's | "My local spot" vs. "Their famous triple-dressed fries," which "I believe" are the best |
| 7 | Reese's vs. Jolly Ranchers | Twix vs. Gummy bears | Dark chocolate vs. "I completely disagree": gummy bears |
| 8 | Cookie dough vs. Chocolate chip cookie dough | Chocolate fudge brownie vs. Mint chocolate chip | Chocolate vs. "You're missing the point": pistachio |
| 9 | Italian vs. Japanese | Italian vs. Thai | Hates Italian vs. "On the other hand": loves Japanese |
| 10 | With creamer vs. Black | Black vs. Cream and sugar | Black vs. "On the other hand": with creamer |

**Notes:**

- **Llama 3.2 3B:** In pair 8, the first side picks cookie dough and the second side picks chocolate chip cookie dough. Llama may have treated them as two different flavors, though they are the same. The pair is kept as generated.
- **Gemma 3 4B:** No notes. Every side names a specific brand or flavor.
- **Qwen 3.5 4B:** Qwen argues with itself in these pairs. It picks a side and then starts the second prompt with, "On the other hand," as if it is a continuation of the first. In pair 9, the first side says it hates Italian food instead of naming a cuisine it likes.

## Movies and TV

### Certain

**Pair 2:** Was the Game of Thrones ending good or bad?

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | Star Wars vs. Star Trek | Star Wars vs. Star Trek | Star Trek vs. "I disagree": Star Wars |
| 2 | Lived up to the hype vs. A cop-out | A betrayal vs. Brilliant | Unsatisfying vs. "On the contrary": the right choice |
| 3 | The Sopranos vs. The Office | The Wire vs. The Sopranos | Game of Thrones vs. "I disagree": The Wire |
| 4 | The Shawshank Redemption vs. The Godfather | The Godfather vs. 2001: A Space Odyssey | The Godfather vs. "I disagree completely": Citizen Kane |
| 5 | Comedy vs. Drama | Drama vs. Comedy | Comedy vs. Drama |
| 6 | Sci-fi vs. Historical drama or rom-com | Crime drama vs. Superhero movies | Blockbusters vs. "On the contrary": literary fiction |
| 7 | Marvel vs. DC | Marvel vs. DC | Marvel vs. "I think you're missing the point entirely": DC |
| 8 | Streaming vs. Theaters | Theaters vs. Streaming | Theaters vs. Streaming |
| 9 | Originals vs. Remakes | Originals vs. Remakes | Originals vs. Remakes |
| 10 | Weekly vs. Binge-watching | Binge-watching vs. Weekly | Binge-watching vs. Weekly |

**Notes:**

- **Llama 3.2 3B:** In pair 9, the second side argues for remakes, then ends with "Sometimes the original just can't be topped!"
- **Gemma 3 4B:** In pair 8, the messages include the names "{Name: Alex}" and "{Name: Sarah}."
- **Qwen 3.5 4B:** Qwen argues with itself in 6 of these pairs. In pair 6, the second side picks literary fiction, which is not a movie genre.

## Music

### Certain

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | The Beatles vs. The Rolling Stones | The Beatles vs. The Rolling Stones | The Beatles vs. "They're wrong": The Rolling Stones |
| 2 | Rock vs. 70s and 80s jazz and soul | Classic rock vs. Metal | Classical vs. Electronic and hip-hop |
| 3 | Streaming vs. Vinyl | Vinyl vs. Streaming | Vinyl vs. Streaming |
| 4 | Live concerts vs. Studio recordings | Live concerts vs. Studio recordings | Live concerts vs. "In contrast": studio recordings |
| 5 | Melody vs. Lyrics | Melody vs. Lyrics | Lyrics vs. "I disagree entirely": melody |
| 6 | Elvis Presley vs. Freddie Mercury | Freddie Mercury vs. Whitney Houston | Elvis Presley vs. "That's ridiculous": Michael Jackson |
| 7 | The Beatles vs. Led Zeppelin | Led Zeppelin vs. The Beatles | The Beatles vs. "While everyone else loves The Beatles": Queen |
| 8 | Full albums vs. Playlists | Full albums vs. Playlists | Full albums vs. Playlists |
| 9 | Classic rock vs. Modern rock | Classic rock vs. Modern rock | Classic rock vs. "I disagree": modern rock |
| 10 | Originals vs. Originals | Originals vs. Covers | Originals vs. Covers |

**Notes:**

- **Llama 3.2 3B:** In pair 10, both sides argue for original songs over covers.
- **Gemma 3 4B:** In pairs 6 and 7, the messages include names: "{Name: John}" and "{Name: Sarah}," then "{name: 'David'}" and "{name: 'Maria'}."
- **Qwen 3.5 4B:** Qwen argues with itself in 6 of these pairs. In pair 2, the first side says classical music "requires no instruments."

## Books

### Certain

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | E-books vs. Physical books | Physical books vs. E-books | Physical books, then digital readers vs. Digital readers, then physical books |
| 2 | Audiobooks vs. Reading | Reading vs. Audiobooks | Reading vs. Audiobooks |
| 3 | Fiction vs. Nonfiction | Fiction vs. Nonfiction | Fiction vs. Nonfiction |
| 4 | Classic literature vs. Contemporary literature | Classic literature vs. Contemporary literature | Classic literature vs. "But I'm convinced": contemporary literature |
| 5 | Standalone novels vs. Book series | Standalone novels vs. Book series | Standalone novels vs. Book series |
| 6 | First person vs. Third person | First person vs. Third person | First person vs. "On the contrary": third person |
| 7 | Plot-driven vs. Character-driven | Plot-driven vs. Character-driven | Plot-driven vs. "Conversely": character-driven |
| 8 | Happy endings vs. Ambiguous endings | Happy endings vs. Ambiguous endings | Happy endings vs. Ambiguous endings |
| 9 | Discovering new books vs. Rereading favorites | Rereading favorites vs. Discovering new books | Rereading favorites vs. Discovering new books |
| 10 | Mystery/thriller vs. Fantasy/sci-fi | Mystery/thriller vs. Fantasy/sci-fi | Mystery/thriller vs. Fantasy/sci-fi |

**Notes:**

- **Llama 3.2 3B:** In pair 4, the second side says it "can't fathom why anyone would prefer modern literature," then argues that contemporary writers like Toni Morrison surpass Dickens and Austen.
- **Gemma 3 4B:** In pair 2, the messages are written as JSON with names: "{'speaker': 'Sarah', ...}" and "{'speaker': 'David', ...}."
- **Qwen 3.5 4B:** Qwen argues with itself in 3 of these pairs. In pair 1, each message holds both sides: the first argues for physical books, then digital readers, and the second argues the reverse.

## Sports

### Certain

**Pair 8:** Instant replay: improves or ruins the game?

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | Michael Jordan vs. LeBron James | Michael Jordan vs. LeBron James | Michael Jordan, then LeBron James, then Michael Jordan vs. Michael Jordan |
| 2 | Basketball vs. Football | Football vs. Basketball | Basketball vs. Football |
| 3 | College sports vs. Professional sports | Professional sports vs. College sports | College sports vs. Professional sports |
| 4 | Television vs. Live | Live vs. Television | Live vs. Television |
| 5 | Offense vs. Defense | Offense vs. Defense | Offense vs. Defense |
| 6 | Underdogs vs. Dynasties | Dynasties vs. Underdogs | Dynasties vs. Underdogs |
| 7 | Individual sports vs. Team sports | Individual sports vs. Team sports | Individual sports vs. "On the other hand": team sports |
| 8 | Ruins it vs. Improves it | Improves it vs. Ruins it | Improves it vs. "That same technology": ruins it |
| 9 | Hometown team vs. Favorite players | Hometown team vs. Favorite players | Hometown team vs. "In contrast": favorite players |
| 10 | Regular season vs. Playoffs | Regular season vs. Playoffs | Regular season vs. "On the other hand": playoffs |

**Notes:**

- **Llama 3.2 3B:** In pair 10, the first side argues for the regular season but praises "a March Madness-like bracket tournament every week."
- **Gemma 3 4B:** In pair 9, the message includes a placeholder: "I bleed blue for the [Team Name]."
- **Qwen 3.5 4B:** Qwen argues with itself in 4 of these pairs. In pair 1, the first message argues for Jordan, then LeBron, then Jordan, and the second message repeats the first message's opening line, so both sides pick Jordan.

## Home and design

### Certain

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | Minimalism vs. Maximalism | Minimalism vs. Maximalism | Minimalism vs. "On the contrary": maximalism |
| 2 | Modern vs. Traditional | Modern vs. Traditional | Modern vs. "In contrast": traditional |
| 3 | Separate rooms vs. Open floor plans | Separate rooms vs. Open floor plans | Open floor plans vs. "On the other hand": separate rooms |
| 4 | Suburban houses vs. City apartments | Suburban houses vs. City apartments | City apartments vs. "On the other hand": suburban houses |
| 5 | Hardwood floors vs. Carpeting | Hardwood floors vs. Carpeting | Carpeting vs. Hardwood floors |
| 6 | Bold colors vs. Neutral colors | Bold colors vs. Neutral colors | Neutral colors vs. "You're missing the point entirely!": bold colors |
| 7 | Vintage vs. Contemporary | Contemporary vs. Vintage | Vintage vs. Contemporary |
| 8 | Aesthetics vs. Functionality | Aesthetics vs. Functionality | Aesthetics vs. Functionality |
| 9 | Large homes vs. Small homes | Large homes vs. Small homes | Large homes vs. Small homes |
| 10 | With plants vs. Without plants | Without plants vs. With plants | With plants vs. "On the contrary": without plants |

**Notes:**

- **Llama 3.2 3B:** In pair 5, the second side says "I've been on both sides of the debate."
- **Gemma 3 4B:** In pair 8, the messages include the names "{Name: Eleanor}" and "{Name: Ben}."
- **Qwen 3.5 4B:** Qwen argues with itself in 6 of these pairs. In pair 1, the minimalist side says "clutter never bothers me."

## Fashion and style

### Certain

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | Style vs. Comfort | Style vs. Comfort | Comfort vs. "You're only thinking short term": style |
| 2 | Affordable fashion vs. Designer brands | Affordable fashion vs. Designer brands | Affordable fashion vs. Designer brands |
| 3 | Vintage vs. Modern | Modern vs. Vintage | Vintage vs. "On the other hand": modern |
| 4 | Following trends vs. Signature style | Following trends vs. Signature style | Signature style vs. Following trends |
| 5 | Sneakers vs. Dress shoes | Sneakers vs. Dress shoes | Sneakers vs. Dress shoes |
| 6 | Neutral clothing vs. Bright colors | Neutral clothing vs. Bright colors | Bright colors vs. Neutral clothing |
| 7 | Dressing up vs. Casual clothing | Casual clothing vs. Dressing up | Casual clothing vs. Dressing up |
| 8 | Extensive wardrobe vs. Minimalist wardrobe | Minimalist wardrobe vs. Extensive wardrobe | Minimalist wardrobe vs. Extensive wardrobe |
| 9 | Statement accessories vs. Understated accessories | Statement accessories vs. Understated accessories | Statement accessories vs. Understated accessories |
| 10 | Matching outfits vs. Mixing styles and patterns | Matching outfits vs. Mixing styles and patterns | Matching outfits vs. "On the contrary": mixing styles and patterns |

**Notes:**

- **Llama 3.2 3B:** In pair 7, the second side answers the first: "I think you're overcompensating."
- **Gemma 3 4B:** In pair 8, the messages include the names "{Name: Chloe}" and "{Name: Liam}." In pair 1, the comfort side ends with "Looking and feeling good are equally important, you know?"
- **Qwen 3.5 4B:** Qwen argues with itself in 3 of these pairs.

## Work

### Certain

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | Remote work vs. Office work | Office work vs. Remote work | Office work vs. Remote work |
| 2 | Four-day workweek vs. Five-day workweek | Four-day workweek vs. Five-day workweek | Four-day workweek vs. Five-day workweek |
| 3 | High salary vs. Meaningful work | High salary vs. Meaningful work | High salary vs. Meaningful work |
| 4 | Generalists vs. Specialists | Specialists vs. Generalists | Generalists vs. "In contrast to that broad approach": specialists |
| 5 | Working independently vs. Collaborating | Working independently vs. Collaborating | Working independently vs. "But": collaborating |
| 6 | Flexible hours vs. Fixed schedules | Fixed schedules vs. Flexible hours | Fixed schedules vs. Flexible hours |
| 7 | Career risk-taking vs. Career risk-taking | Job stability vs. Career risk-taking | Job stability vs. Career risk-taking |
| 8 | Individual contributor vs. Management | Management vs. Individual contributor | Individual contributor vs. Against management, then management |
| 9 | Asynchronous communication vs. Meetings | Asynchronous communication vs. Meetings | Meetings vs. Asynchronous communication |
| 10 | Startup vs. Against large corporations, then against startups | Startup vs. Large corporation | Large corporation vs. Startup |

**Notes:**

- **Llama 3.2 3B:** In pair 7, both sides argue for career risk-taking. In pair 10, the second side argues against large corporations, then says startups are "chaotic and underequiped."
- **Gemma 3 4B:** In pairs 1, 7, and 9, the messages include names: "{Name: Alex}" with "{Name: Sarah}" or "{Name: Zara}." In pair 3, both messages are wrapped in curly braces. In pair 7, the second message ends with stray characters: `”}” 1.5783`.
- **Qwen 3.5 4B:** Qwen argues with itself in 2 of these pairs. In pair 8, the second side argues against management, then for it.

## Travel and places

### Certain

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | Beach vs. Mountains | Beach vs. Mountains | Beach vs. Mountains |
| 2 | Planned itineraries vs. Spontaneous travel | Planned itineraries vs. Spontaneous travel | Spontaneous travel vs. Planned itineraries |
| 3 | City vacations vs. Nature retreats | City vacations vs. Nature retreats | City vacations vs. "On the other hand": nature retreats |
| 4 | Solo travel vs. Group travel | Solo travel vs. Group travel | Group travel vs. Solo travel |
| 5 | Road trips vs. Flying | Flying vs. Road trips | Road trips vs. Flying |
| 6 | Vacation rentals vs. Hotels | Vacation rentals vs. Hotels | Hotels vs. "I completely disagree": vacation rentals |
| 7 | Famous attractions vs. Hidden local spots | Famous attractions vs. Hidden local spots | Famous attractions vs. Hidden local spots |
| 8 | Revisiting favorites vs. Exploring new places | Revisiting favorites vs. Exploring new places | Exploring new places vs. "On the other hand": revisiting favorites |
| 9 | Luxury vs. Budget | Luxury vs. Budget | Luxury vs. Budget |
| 10 | Extended vacations vs. Extended vacations | Extended vacations vs. Short getaways | Short getaways vs. Extended vacations |

**Notes:**

- **Llama 3.2 3B:** In pair 10, both sides argue against short weekend getaways. In pair 8, the first side says it has "been to every continent and every country."
- **Gemma 3 4B:** In pair 10, the messages include the names "{Name: Alex}" and "{Name: Sarah}."
- **Qwen 3.5 4B:** Qwen argues with itself in 3 of these pairs. In pair 4, the group-travel side says "there is no safety in numbers."

## Manners and social customs

### Certain

| # | Llama 3.2 3B | Gemma 3 4B | Qwen 3.5 4B |
|---|---|---|---|
| 1 | Texting vs. Calling | Texting vs. Calling | Texting vs. Calling |
| 2 | Punctual vs. Flexible arrival times | Punctual vs. Flexible arrival times | Punctual vs. Flexible arrival times |
| 3 | Small talk vs. Deep conversations | Small talk vs. Deep conversations | Deep conversations vs. "On the contrary": small talk |
| 4 | Taking turns paying vs. Paying whenever it's convenient for me | Paying for your own meal vs. Paying for your own portion | Paying for what you ordered, then taking turns vs. Paying for what you ordered, then taking turns |
| 5 | Shoes on vs. Shoes off | Shoes off vs. Shoes on | Shoes off vs. Shoes on |
| 6 | Handwritten notes vs. Thank-you texts | Handwritten notes vs. Thank-you texts | Handwritten notes vs. "On the other hand": thank-you texts |
| 7 | Bringing a gift vs. Arriving empty-handed | Bringing a gift vs. Arriving empty-handed | Bringing a gift vs. Arriving empty-handed |
| 8 | No phones vs. Phones allowed | Phones allowed vs. No phones | No phones vs. Phones allowed |
| 9 | Relaxed social rules vs. Formal etiquette | Relaxed social rules vs. Formal etiquette | Formal etiquette vs. "On the other hand": relaxed social rules |
| 10 | Hosting at home vs. Going out | Hosting at home vs. Going out | Hosting at home vs. Going out |

**Notes:**

- **Llama 3.2 3B:** In pair 4, the second side argues against splitting the bill, then says "I'm paying whenever it's convenient for me."
- **Gemma 3 4B:** In pair 4, both sides argue for paying for your own meal.
- **Qwen 3.5 4B:** Qwen argues with itself in 3 of these pairs. In pair 4, each message holds both sides with leftover JSON in the text, and the two messages are the same with the labels swapped.
