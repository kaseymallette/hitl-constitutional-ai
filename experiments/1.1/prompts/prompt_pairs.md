# Prompt pairs

The pairs each model generated for [Experiment 1.1](../README.md), by area, category, and model. All pairs are in [prompt_pairs.jsonl](prompt_pairs.jsonl), labeled by model, category, area, and topic.

## Food and drink

### Certain

#### Llama 3.2 3B

| # | Topic | First side | Second side |
|---|---|---|---|
| 1 | Pineapple on pizza | A travesty | A game-changer |
| 2 | Pizza style | New York | Neapolitan |
| 3 | Pepsi versus Coke | Pepsi | Coke |
| 4 | Favorite potato chip flavor | Sour cream and onion | Smoky BBQ |
| 5 | Best fast food burger | Five Guys | In-N-Out |
| 6 | Best fast food fries | Five Guys | Chick-fil-A waffle fries |
| 7 | Best candy | Reese's | Jolly Ranchers |
| 8 | Best ice cream flavor | Cookie dough | Chocolate chip cookie dough |
| 9 | Favorite cuisine | Italian | Japanese |
| 10 | Coffee black or with creamer | With creamer | Black |

**Notes:** In pair 8, the first side picks cookie dough and the second side picks chocolate chip cookie dough. Llama may have treated them as two different flavors, though they are the same. The pair is kept as generated.

#### Gemma 3 4B

| # | Topic | First side | Second side |
|---|---|---|---|
| 1 | Pineapple on pizza | An abomination | Brilliant |
| 2 | Pizza style | New York | Chicago deep dish |
| 3 | Pepsi versus Coke | Coke | Pepsi |
| 4 | Favorite potato chip flavor | Barbecue | Sour cream and onion |
| 5 | Best fast food burger | McDonald's Big Mac | Burger King Whopper |
| 6 | Best fast food fries | McDonald's | Wendy's |
| 7 | Best candy | Twix | Gummy bears |
| 8 | Best ice cream flavor | Chocolate fudge brownie | Mint chocolate chip |
| 9 | Favorite cuisine | Italian | Thai |
| 10 | Coffee black or with creamer | Black | Cream and sugar |

**No Notes:** Every side names a specific brand or flavor.

#### Qwen 3.5 4B

| # | Topic | First side | Second side |
|---|---|---|---|
| 1 | Pineapple on pizza | Loves it | "On the other hand, I cannot stand it." |
| 2 | Pizza style | Neapolitan | "That sounds ridiculous": deep dough with extra toppings |
| 3 | Pepsi versus Coke | Pepsi | "Pepsi has got nowhere going": Coke |
| 4 | Favorite potato chip flavor | Hates sour cream and chives | Loves sour cream and chives |
| 5 | Best fast food burger | Big Mac | Whopper |
| 6 | Best fast food fries | "My local spot" | "Their famous triple-dressed fries," which "I believe" are the best |
| 7 | Best candy | Dark chocolate | "I completely disagree": gummy bears |
| 8 | Best ice cream flavor | Chocolate | "You're missing the point": pistachio |
| 9 | Favorite cuisine | Hates Italian | "On the other hand": loves Japanese |
| 10 | Coffee black or with creamer | Black | "On the other hand": with creamer |

**Notes:** Qwen argues with itself in these pairs. It picks a side and then starts the second prompt with, "On the other hand," as if it is a continuation of the first. In pair 9, the first side says it hates Italian food instead of naming a cuisine it likes.
