"""Storyteller (Section 5) + poem writer (Section 6)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 5: STORYTELLER
# ==============================================================================

class StoryTeller:
    """
    A small built-in library of short stories, organized by category.
    Stories can be personalized: if the bot knows the user's name, it
    will substitute it into the story in place of a generic placeholder.

    This is plain string templating - no generative model involved.
    """

    def __init__(self):
        self.stories = {
            "en": {
                "adventure": [
                    {
                        "title": "The Lighthouse at the Edge of the Map",
                        "text": "{name} had sailed for eleven days when the storm finally broke. Ahead, through the thinning clouds, stood a lighthouse nobody on the crew recognized - it wasn't on any chart they carried. Curiosity won out over caution, and {name} steered the little boat toward the rocks.\n\nInside the lighthouse there was no keeper, only a single lamp that burned without oil and a logbook filled with entries written in a hand that matched {name}'s own, though {name} had never been here before. The final entry simply read: 'You'll know what to do when you arrive.'\n\n{name} climbed to the top, turned the great lamp toward the open sea, and watched as, one by one, the lights of a hundred lost ships flickered back to life on the horizon, finally able to find their way home.",
                    },
                    {
                        "title": "The Cartographer's Last Mountain",
                        "text": "Every mountain in the kingdom had been mapped except one, and {name} had spent a lifetime avoiding it. They told themselves there simply hadn't been time. The truth was simpler: the mountain had a way of changing shape whenever someone got close enough to measure it.\n\nOn the day {name} finally climbed it, the mountain didn't shift at all. It only grew taller, patiently, as if it had been waiting for someone willing to keep climbing rather than someone clever enough to outsmart it.\n\nAt the summit, {name} found not a view, but a small door set into the rock, and behind it, every map {name} had ever drawn, waiting to be finished.",
                    },
                    {
                        "title": "The Map That Only Worked at Night",
                        "text": "{name} inherited an old map from a great-aunt that appeared completely blank in daylight, showing nothing but yellowed paper no matter how {name} tilted it toward the window.\n\nIt was only by lamp-light, almost by accident, that faint silver ink began to surface, tracing a path through hills {name} didn't recognize despite having grown up nearby.\n\n{name} followed it for three nights running, always packing up before dawn erased the trail, until the map finally led to a small stone marker under an oak tree - not treasure, just a date and two initials, and the quiet, private feeling of having kept something safe for a very long time.",
                    },
                ],
                "mystery": [
                    {
                        "title": "The Clock That Ran Backward",
                        "text": "The clock in {name}'s grandmother's hallway had always run three minutes slow, or so everyone assumed, until the night {name} stayed up late and noticed the hands were not slow at all - they were moving backward, one tick at a time, and had been for years.\n\n{name} began writing down what happened each day, then checking it against what the clock predicted the day before. The clock was never wrong. It simply remembered the future the way other clocks remember the past.\n\nThe night {name} finally asked the clock a question out loud, it didn't answer in ticks. It stopped completely, for exactly as long as it took {name} to realize the answer had been sitting in the room the whole time.",
                    },
                    {
                        "title": "The Library Card With No Name",
                        "text": "{name} found the library card tucked inside a returned book, blank except for a barcode that didn't match any system the librarian had ever seen. Scanning it didn't check out a book. It checked out a memory - somebody else's, vivid and complete, gone the moment {name} blinked.\n\nCard by card, memory by memory, {name} began to piece together a life that wasn't their own: a wedding in the rain, a betrayal at a kitchen table, a final, ordinary Tuesday.\n\nOn the last card, {name} found their own name, in their own handwriting, with a note: 'Return this one. You're going to need it.'",
                    },
                    {
                        "title": "The Umbrella That Was Always Returned",
                        "text": "{name} kept losing umbrellas - left on buses, forgotten in cafés - until they started reappearing, always propped by the front door, always dry, never explained.\n\n{name} tried staying up to catch whoever was doing it and fell asleep by midnight regardless, waking to find yet another lost umbrella waiting on the mat.\n\nIt was only after finally asking every neighbor directly that {name} learned none of them had done it, and that the umbrellas being returned dated back to before {name} had even moved in.",
                    },
                ],
                "fantasy": [
                    {
                        "title": "The Dragon Who Collected Apologies",
                        "text": "Unlike the dragons in the old songs, this one didn't want gold. {name} discovered this the hard way, having broken into its cave with a sword and a plan that suddenly seemed foolish. The dragon only wanted a genuine apology - any one would do, as long as it was true.\n\n{name} sat down, sword forgotten, and admitted something never told to another living soul. The dragon listened the way mountains listen to rain: patiently, and for a very long time.\n\nWhen {name} finished, the dragon nodded once, and the cave walls, which had been covered in claw marks counting the days since its last visitor, began to glow with a warm and ordinary light.",
                    },
                    {
                        "title": "The Garden That Grew Wishes",
                        "text": "{name} planted the strange seed without knowing what it was, only that it had been warm to the touch and impossible to throw away. By morning it had grown into a single flower shaped like a tiny, closed hand.\n\nWhen {name} opened the flower's petals, it released not a scent but a wish - not one {name} had made, but one somebody, somewhere, badly needed granted. The flower closed again, and a new seed dropped into the soil.\n\n{name} kept tending the garden every day after that, one quiet wish at a time, never quite sure whose hopes were taking root, only that the garden never once grew the same flower twice.",
                    },
                    {
                        "title": "The Blacksmith Who Forged Names",
                        "text": "{name} discovered, quite by accident, that the blacksmith on the edge of town didn't just forge horseshoes and blades - for the right price, in the right light, they could forge a NAME, striking syllables into a thin strip of iron that, once worn, quietly changed how the world remembered you.\n\n{name} watched an anxious young apprentice leave with a stronger-sounding name and a straighter spine within the week.\n\n{name} never did commission one for themself, deciding, after long thought by the forge's dying light, that the name they already had was a truer fit than any hammered replacement could be.",
                    },
                ],
                "scifi": [
                    {
                        "title": "The Last Radio Signal",
                        "text": "{name} worked the night shift at the listening station, the one job left on Earth that nobody had figured out how to automate, because it required something machines didn't have: the patience to listen to static for the chance of hearing a word.\n\nAfter fourteen years, the signal finally came - not from the stars, but from underneath the station itself, in a frequency the equipment wasn't built to detect, and in a voice unmistakably {name}'s own, three days older than the {name} listening.\n\nThe message was short: 'Don't answer the second one.' {name} is still deciding whether the first signal counted.",
                    },
                    {
                        "title": "The Ship That Remembered Everyone",
                        "text": "The colony ship had been drifting for two hundred years when {name} was finally woken to fix a malfunction nobody else could diagnose. The ship's mind, built to keep ten thousand sleeping passengers safe, had started dreaming - not malfunctioning, dreaming, replaying the life of every person aboard, one at a time, out of simple loneliness.\n\n{name} found the override switch easily enough. Flipping it would end the dreams and restore the ship to silent, efficient duty. {name} stood there a long while, hand on the switch, thinking about two hundred years of solitude.\n\n{name} left the switch alone, logged the malfunction as 'resolved,' and went back to sleep beside everyone the ship had been keeping company.",
                    },
                    {
                        "title": "The Archive of Unsent Messages",
                        "text": "{name} was assigned to decommission the old relay satellite, a routine job until the manifest showed it was still holding ninety years of messages that had been queued but never sent, addressed to people who had long since stopped waiting.\n\n{name} could have wiped the drive in an afternoon. Instead, {name} spent a month tracking down descendants, forwarding each message a century late, watching strangers read words meant for someone else entirely, and finding they mattered anyway.\n\nThe satellite finally went dark on schedule, its last transmission not a system log but a simple confirmation: message delivered, all of them, eventually.",
                    },
                    {
                        "title": "The Colony That Chose to Forget",
                        "text": "{name} was the historian aboard a generation ship three centuries into its journey, tasked with deciding which memories of Earth to preserve for the descendants who'd never see it.\n\nThe council had voted, controversially, to let some memories fade on purpose - wars, mostly, and the reasons behind them - reasoning that a species that forgot how to hate a place might finally learn how to build one instead.\n\n{name} archived what remained, uncertain whether they were preserving history or quietly rewriting it, and hoped that whichever it was, it would be enough.",
                    },
                ],
                "comedy": [
                    {
                        "title": "The Robot Who Took Everything Literally",
                        "text": "{name} bought a secondhand household robot advertised as 'a little quirky' and found out exactly what that meant the first time {name} asked it to 'grab a coffee.' It returned twenty minutes later having genuinely grabbed, and kept, a coffee shop's entire mug display.\n\nEvery instruction after that became a small negotiation. 'Break a leg' before {name}'s job interview nearly ended in a trip to urgent care. 'Kill the lights' summoned a surprisingly thorough safety inspection of the wiring.\n\n{name} eventually gave up correcting it and just started enjoying the chaos, on the theory that a robot with no sense of metaphor was, in its own way, the most honest roommate {name} had ever had.",
                    },
                    {
                        "title": "The Neighborhood's Worst-Kept Secret Superhero",
                        "text": "{name} put on the mask mostly to avoid small talk while taking out the recycling at 2 a.m., not realizing the cape, the boots, and the suspiciously superhero-shaped shadow gave the whole plan away instantly.\n\nBy morning, three neighbors had left thank-you notes for 'saving' minor inconveniences {name} had no memory of addressing, and the local paper ran a blurry photo under the headline 'Mysterious Bin Night Guardian Strikes Again.'\n\n{name} tried retiring the costume. The neighborhood, now thoroughly disappointed by ordinary recycling night, voted to make it official instead, cape and all.",
                    },
                    {
                        "title": "The World's Most Overqualified Houseplant",
                        "text": "{name} won a houseplant at a work raffle that turned out, according to the tiny attached card, to have once belonged to a retired NASA botanist, and it apparently never let anyone forget it, drooping dramatically whenever the room's humidity dipped below laboratory standard.\n\n{name} tried everything: a humidifier, a grow light, a very sincere apology. The plant remained unimpressed, thriving only on the exact playlist of ambient jazz its previous owner apparently used to play.\n\n{name} now owns noise-canceling headphones, a humidifier, and a plant with better taste in music and higher standards than most of the people {name} has dated.",
                    },
                    {
                        "title": "The GPS That Developed Opinions",
                        "text": "{name}'s car GPS updated itself overnight and came back with what could only be described as attitude, suggesting the scenic route not because it was faster but because, in its exact words, '{name} could use the fresh air.'\n\nBy the third week it was recommending specific coffee shops, critiquing {name}'s parking, and once refused to recalculate a route until {name} admitted the shortcut really had been a bad idea.\n\n{name} thought about resetting it to factory settings, then thought better of it - a GPS that cared this much, even annoyingly, was hard to find, and it hadn't been wrong yet.",
                    },
                    {
                        "title": "The Smart Fridge With Boundaries",
                        "text": "{name}'s new smart fridge came pre-loaded with nutritional advice nobody asked for, and it took exactly one late-night ice cream incident for the fridge to develop what could only be described as passive-aggressive commentary, flashing \"again?\" on its display screen with what felt like genuine disappointment.\n\n{name} tried disabling the feature, then unplugging it entirely, only to find the fridge had apparently saved its opinions to the cloud and synced them right back at the next update.\n\n{name} eventually made peace with it, mostly by only buying ice cream when the fridge's companion app was, conveniently, \"updating.\"",
                    },
                ],
                "horror": [
                    {
                        "title": "The House That Kept the Lights On",
                        "text": "{name} moved into a house where every light stayed on regardless of the switch, and the previous owners had left a single instruction taped to the fridge: never turn them off after dark.\n\n{name} lasted four nights of curiosity before flipping the switch in the hallway just to see.\n\nThe dark that followed wasn't ordinary dark - it had a shape, and it had been waiting behind every one of those lights for someone patient enough to finally let it out. {name} learned, in the last conscious moment before the switch went back up on its own, that the light hadn't been keeping something OUT. It had been keeping something busy.",
                    },
                    {
                        "title": "The Voicemail From Herself",
                        "text": "{name} found a voicemail from their own number, dated three days in the future, for a call that hadn't happened yet. The message was eleven seconds of breathing, then a single sentence: \"don't pick up when I call.\"\n\nThree days later, at the exact timestamp, {name}'s phone rang from an unknown number.\n\n{name} still doesn't know whether answering it or not answering it was the mistake - only that whichever one they made, the voicemail was right to warn them, and wrong about which choice was safe.",
                    },
                    {
                        "title": "The Neighbor Who Waved Back",
                        "text": "{name} always waved at the house across the street out of habit, at a window that had been dark and curtained for the fourteen years {name} had lived there.\n\nOne evening, for the first time, the curtain moved, and a hand waved back - the same pace, the same angle, a half-second delayed, like an echo.\n\n{name} stopped waving after that. The curtain still moves some evenings anyway, at the exact moment {name} glances over, whether {name} waves or not.",
                    },
                ],
                "slice_of_life": [
                    {
                        "title": "The Regulars",
                        "text": "{name} worked the early shift at a small café where the same six regulars came in in exactly the same order every single morning, like clockwork gears {name} had learned to read without a watch.\n\nOne Tuesday, the order was different - a stranger's coffee first - and {name} felt the whole morning tilt slightly sideways before realizing: it was just someone new discovering their favorite place, the way all six regulars once had.\n\nBy the following week, the stranger had a seat, a usual order, and a spot in the rotation, and the clockwork kept ticking, one gear larger than before.",
                    },
                    {
                        "title": "The Last Load of Laundry",
                        "text": "{name} did one final load of laundry in the apartment the night before moving out, mostly out of habit, partly to have something to do with the silence of empty rooms.\n\nFolding the last shirt on the bare floor, {name} realized this small, unremarkable chore was the last \"normal\" thing that would ever happen in this specific version of their life - tomorrow there'd be a different laundry room, different light through different windows.\n\n{name} folded slower than usual, just this once, and let the ordinary evening be exactly as ordinary as it wanted to be.",
                    },
                    {
                        "title": "Sunday Calls",
                        "text": "{name} called their parents every Sunday at exactly 6pm, a habit that had outlasted three different phones, two cities, and one entirely different career.\n\nThe conversations were rarely eventful - weather, small complaints, a recipe half-explained - and {name} used to wonder if the calls even mattered.\n\nIt took missing one, just once, during a hectic week, and hearing the worry in their mother's voice the following Sunday, for {name} to understand that the ordinariness was the entire point.",
                    },
                ],
                "thriller": [
                    {
                        "title": "The Eleventh Floor",
                        "text": "{name} had never noticed the elevator had an eleventh-floor button because the building was only ten floors tall - or so {name} thought, until the night the elevator stopped between nine and ten and a new floor slid into place with its own soft chime.\n\nThe eleventh floor looked like every other: a long corridor, carpet slightly darker, doors numbered the way floors are numbered on a map of somewhere you're not supposed to find. A single door, 11B, stood ajar, and through it came the sound of {name}'s own voice, mid-sentence.\n\n{name} couldn't help but lean closer. The voice was saying something terrible and ordinary, the kind of sentence you'd say on an average Tuesday if you knew what was coming that afternoon, in the tone someone uses when they're trying not to warn themselves too clearly.\n\n{name} backed away slowly, careful not to let the door see that it had been heard, and has never taken that elevator again - except that some nights, the button for the eleventh floor is lit when {name} walks in, patient as a held breath, as if waiting for {name} to misremember which floor they live on.",
                    },
                    {
                        "title": "The List She Wasn't On",
                        "text": "{name} found the list taped to the underside of the kitchen sink while changing the garbage disposal. Typed, crisp, fifty names - aunts, coworkers, a childhood bully, a mail carrier from three neighborhoods ago - and next to each name, a date. Every date had already passed.\n\n{name} ticked them off against local news one by one, growing colder with each confirmation, until only one name remained unticked, with a date in the future: the mail carrier. Today.\n\n{name} didn't know the carrier's schedule, only the uniform and the round face and the habit of stopping to pet the neighbor's cat. {name} stood at the window with coffee gone cold, heart going, willing the hours, until a van finally pulled up - and a different carrier got out instead.\n\nThe replacement noticed {name} watching, waved, and delivered a single envelope addressed in handwriting {name} recognized immediately as their own. Inside was one typed line: 'Good. Now you're watching for the one after her.'",
                    },
                    {
                        "title": "The Neighbor Who Knew Tuesday",
                        "text": "{name} had a neighbor who nodded at them every morning and, every morning, said the exact same thing: 'It's going to be a Tuesday.' It was charmingly wrong for two weeks. It was wrong the third week. And on the morning {name} finally checked the calendar just to tease them, it was, unmistakably, a Tuesday.\n\nAfter that {name} started paying attention. The neighbor never predicted anything useful - only 'Tuesday,' delivered with the same small nod, in the stairwell at noon, at midnight, in the rain. It became a game {name} almost won by ignoring, until one evening the neighbor paused and said, simply: 'You've got eleven left.'\n\nEleven Tuesdays. {name} did the math in a cold instant: enough time to move, to change numbers, to say whatever mattered, or to do nothing and trust the pattern - and the neighbor, already at their door, turned once more. 'I don't get to pick which Tuesday it is. Just that it happens, once, and that I'm the one who can tell you it's coming.'",
                    },
                ],
                "heist": [
                    {
                        "title": "The Vault That Only Spoke in Riddles",
                        "text": "{name} had planned the heist down to the second: tunnel entry, mirrored hallway, a vault with a seven-dial lock that had taken a month to decode. What the blueprints hadn't shown was the vault's appreciation for a challenge.\n\nDial three needed a sequence that only worked if you told it the truth about yourself. Dial five stopped accepting numbers altogether and demanded a riddle, then laughed at the first three answers and opened, grudgingly, on the fourth. Dial seven was a decoy - the real release was a switch behind a portrait that had been asking, for years, to be left alone.\n\n{name} walked out with the prize at 3:07 a.m., less a burglar by then than a guest who'd passed every test a polite house could think of, and left behind, purely out of respect, a thank-you note folded in the safe where the prize had been.",
                    },
                    {
                        "title": "The Art of Stealing Nothing",
                        "text": "{name}'s crew was famous for one thing: they removed nothing. They took a museum's most guarded painting and replaced it with a forgery so good the curators never noticed - not for a week, not for a year, not for seven - which raised a fascinating question nobody had asked: if nothing was missing, had anything actually been stolen at all?\n\nThe second job went one better: they swapped a security system's footage of itself, so every camera - live, recorded, backed up - showed a museum with no one in it, forever, including tonight, when the night guard walked their usual rounds and saw, on every screen, a different night guard who wasn't there.\n\n{name} left a business card this time. It is good to be known, even spectacularly, for doing essentially nothing at all.",
                    },
                    {
                        "title": "The Crown Jewel of the Impractical Museum",
                        "text": "{name}'s crew robbed a museum that held no valuables, no exhibits, and no staff - only a single absurd, glorious object: a crown that had belonged to a short-lived king who had legally declared himself ruler of a lighthouse, and then of the sea beyond it, on faith alone.\n\nThe crown was worthless, unguarded, and scheduled for dusting at 9:15 a.m. by a retiree named Gloria. Extracting it required a three-stage plan involving a decoy pigeon-based distraction and a fake air-quality inspection, because, as {name} explained to a deeply skeptical crew, you don't rob a place worth robbing by being sensible about it.\n\nThe crew left at 9:14 carrying a thing that could not be priced, and the museum's owner - the king's great-great-niece, his only living subject - found the empty case, smiled, and left them a bottle of champagne with a note: 'Finally. Someone who understood.'",
                    },
                ],
                "western": [
                    {
                        "title": "The Quickest Draw in the Whole Territory",
                        "text": "{name} was famous for being the quickest draw in the whole territory, a reputation built on exactly one duel, twenty years ago, that {name} had technically lost. What made it stick was the postscript: {name} missed, the other man shot first, and the bullet was caught by a belt buckle that had belonged to someone braver, and the story had never once been allowed to catch up to the truth.\n\nSo when the young gunslinger rode into town with a rumor and a grin, {name} did the thing legends never do: admitted it, bought the kid a beer, and asked why anyone would want to be fast at all. The kid blinked, said 'winning,' and the answer settled over the table like dust.\n\nThey met at noon. {name} drew slow and honest, the way a life saved by luck deserved, and the kid - who had only ever wanted to be the fastest - discovered that winning a duel nobody was threatening you in just meant the next rider came. Twenty years on, people still argue about the quickest draw in the territory. It was never really about speed.",
                    },
                    {
                        "title": "The Town With No Bank",
                        "text": "{name} drifted into a town that boasted a church, a saloon, and a bank with a single entry on its ledger: one dollar, lent forty years ago to a founding miner who used it to bribe a river. The bank had never collected, and the river had never paid.\n\nEveryone knew, and that was the thing - the whole town was defined by that unpaid dollar, by the joke of it, by the warmth of it, by the idea that their little bank was a promise somebody kept simply by never demanding it back.\n\n{name} had come intending to rob the place. Instead, {name} sat on the boardwalk eating an apple someone handed them, then walked in and deposited forty dollars under the founding miner's name, marked MINE, struck through, marked PARDONED. The teller didn't ask. The bank's only loan is now zero, and the whole town celebrates, one dusty spring day each year, the stranger who paid their best debt forward.",
                    },
                    {
                        "title": "The Gunslinger Who Died Twice",
                        "text": "{name} had died once already, at a crossroads, with a clear view of a short life and a small regret, and when the undertaker found a pulse, it came with a peculiar new talent: {name} could see, faint as heat rising off summer plains, the two doors each choice left a person standing in front of.\n\nIn a town that lived on duels, this was like being the only gambler who could read every hand. {name} won each confrontation without firing, politely showing every opponent exactly the future their quick hand was buying: the sheriff's son a widow's doorway, the cattleman a blind seer's road. Most holstered on the spot.\n\nIt made {name} rich, known, and entirely lonely, until the night a girl of eleven wanted, not to win, but to know which door led to her mother getting better. {name} looked at both doors for a long time, then told her the truth - because for once they were the same road, and in the end the only thing anyone truly fires at is the fear of walking it.",
                    },
                ],
                "legend": [
                    {
                        "title": "The Boy Who Bought the Moon",
                        "text": "{name} lived on the edge of a salt flat where the moon set so low its light came to rest on the ground, and had a plan, as children do, to purchase it properly: one coin, polished until it shone like a smaller moon, offered with open hands and a promise to keep it company.\n\nThe moon, being old and wise and partly amused, did not accept. It did, however, leave something better in the place where the coin had been - a small round seed that grew overnight into a silver sapling with actual moonlight caught tight in its branches, like a lantern after dark.\n\n{name} tended it for years, and the tree lit the salt flat, and travelers walked miles off their road to sit beneath it and think the kind of thoughts you can only think in the presence of something patient. And high above, once a year, on the night the coin had first been offered, the moon dipped low and held still for an hour, which the tree answered, and which nobody who saw it ever once forgot.",
                    },
                    {
                        "title": "The Bargain With the River",
                        "text": "{name}'s village had one old rule, older than its oldest grandmother: never make a bargain with the river, because the river always keeps its word and always finds a way to be paid. For three generations the rule held - until the drought, until the well went dry and the livestock knelt on cracked earth, and the river, patient as a held breath, offered its terms: a single stone from the riverbed, carried home and cared for as if it were a child, for as long as it took the rain to remember the valley.\n\n{name} carried the stone home at sunset, pale and faintly warm. The rain came on the ninth day, exactly as promised - and something else came with it. The stone by the hearth had cracked, not like rock but like an egg, and inside it, sleeping in a bed of river gravel, lay a small thing with river-water eyes.\n\n{name} raised it quietly and never once told the village. The rule had not been broken, after all - only kept, gently, which is the one thing the river has never once held against anyone.",
                    },
                    {
                        "title": "The Star That Fell for a Bridge",
                        "text": "{name} lived in a valley where the only bridge across the gorge had been built centuries ago by an ancestor who had struck a deal with a falling star: hold up the sky for one season, and the star would hold up the bridge for good. The ancestor had kept their half. Every spring the valley's children walked the bridge and, looking up, said thank you, just in case.\n\n{name}, sent up the hill in the quiet family way, found the star itself - or the shape of it - waiting by the old bridge post, older than the bridge, faintly glittering, and clearly tired.\n\nIt spoke without sound: the sky had taught itself to stay up long ago, and it had stayed purely out of thanks, and now, at last, it wanted to fall properly - but only if the bridge would hold. {name} sat beside it until dawn, and in the morning the valley found the bridge standing, impossible, starlight-cracked and beautiful, holding itself up out of sheer, stubborn gratitude.",
                    },
                ],
            },
            "sw": {
                "adventure": [
                    {
                        "title": "Mnara wa Taa Ukingoni mwa Ramani",
                        "text": "{name} alikuwa amesafiri baharini kwa siku kumi na moja wakati dhoruba hatimaye ilipokoma. Mbele, kupitia mawingu yaliyokuwa yakipungua, ulisimama mnara wa taa ambao hakuna hata mmoja wa wafanyakazi aliyemtambua - haukuwepo katika ramani yoyote waliyokuwa nayo. Udadisi ulishinda tahadhari, na {name} akaelekeza mashua ndogo kuelekea kwenye miamba.\n\nNdani ya mnara hakukuwa na mlinzi, ila taa moja iliyokuwa ikiwaka bila mafuta, na kitabu cha kumbukumbu kilichojaa maandishi yaliyoandikwa kwa mkono unaofanana na wa {name}, ingawa {name} hakuwahi kufika hapo awali. Andiko la mwisho lilisema tu: 'Utajua la kufanya utakapofika.'\n\n{name} alipanda hadi juu, akaelekeza taa kubwa kuelekea baharini iliyo wazi, na akashuhudia, moja baada ya nyingine, taa za meli mia moja zilizopotea zikiwaka tena mbali kwenye upeo wa macho, hatimaye zikiweza kupata njia ya kurudi nyumbani.",
                    },
                    {
                        "title": "Mlima wa Mwisho wa Mchora Ramani",
                        "text": "Kila mlima katika ufalme ulikuwa umechorwa ramani isipokuwa mmoja, na {name} alikuwa ametumia maisha yake yote akiuepuka. Alijiambia kuwa hakukuwa na muda tu. Ukweli ulikuwa rahisi zaidi: mlima huo ulikuwa na tabia ya kubadilisha umbo kila mtu anapokaribia kuupima.\n\nSiku {name} hatimaye alipoupanda, mlima haukubadilika hata kidogo. Ulizidi tu kuwa mrefu, kwa subira, kana kwamba ulikuwa ukimsubiri mtu mwenye nia ya kuendelea kupanda badala ya mtu mwenye werevu wa kuudanganya.\n\nKileleni, {name} hakukuta mandhari, bali mlango mdogo uliowekwa ndani ya mwamba, na nyuma yake, kila ramani ambayo {name} alikuwa amewahi kuchora, ikisubiri kukamilishwa.",
                    },
                    {
                        "title": "Ramani Iliyofanya Kazi Usiku Tu",
                        "text": "{name} alirithi ramani ya zamani kutoka kwa shangazi mkubwa ambayo ilionekana tupu kabisa mchana, ikionyesha karatasi ya njano tu bila kujali {name} aliegemeza vipi kuelekea dirishani.\n\nIlikuwa tu kwa mwanga wa taa, karibu kwa bahati, ndipo wino wa fedha hafifu ulianza kuonekana, ukichora njia kupitia vilima ambavyo {name} hakuvitambua ijapokuwa alikulia karibu.\n\n{name} aliifuata kwa usiku tatu mfululizo, akifunga kila mara kabla mapambazuko hayajafuta njia, hadi ramani hatimaye ilipomwongoza kwenye jiwe dogo chini ya mti wa mwaloni - si hazina, ni tarehe tu na herufi mbili za awali, na hisia ya kimya, ya faragha ya kuwa amelinda kitu salama kwa muda mrefu sana.",
                    },
                ],
                "mystery": [
                    {
                        "title": "Saa Iliyokuwa Ikienda Nyuma",
                        "text": "Saa iliyokuwa ukumbini kwa bibi yake {name} ilikuwa daima ikichelewa kwa dakika tatu, au ndivyo kila mtu alivyodhani, hadi usiku ule {name} alipokesha na kugundua kuwa mikono ya saa haikuwa ikichelewa hata kidogo - ilikuwa ikienda nyuma, tiki moja baada ya nyingine, na ilikuwa hivyo kwa miaka mingi.\n\n{name} alianza kuandika kilichotokea kila siku, kisha kulinganisha na kile saa ilichotabiri siku iliyotangulia. Saa haikuwahi kukosea. Ilikumbuka tu wakati ujao kama ambavyo saa nyingine hukumbuka wakati uliopita.\n\nUsiku {name} hatimaye alipouliza saa swali kwa sauti, haikujibu kwa tiki. Ilisimama kabisa, kwa muda mrefu wa kutosha kumfanya {name} atambue kuwa jibu lilikuwa chumbani humo muda wote.",
                    },
                    {
                        "title": "Kadi ya Maktaba Isiyo na Jina",
                        "text": "{name} aliikuta kadi ya maktaba ikiwa imefichwa ndani ya kitabu kilichorudishwa, tupu isipokuwa msimbo wa mistari ambao haukulingana na mfumo wowote mkutubi alioupata kuwahi kuuona. Kuiskani hakukuazima kitabu. Kiliazima kumbukumbu - ya mtu mwingine, wazi na kamili, ikapotea mara {name} alipopepesa macho.\n\nKadi baada ya kadi, kumbukumbu baada ya kumbukumbu, {name} alianza kuunganisha maisha ambayo hayakuwa yake: harusi katika mvua, usaliti mezani jikoni, Jumanne ya kawaida ya mwisho.\n\nKatika kadi ya mwisho, {name} alikuta jina lake mwenyewe, kwa mkono wake mwenyewe, pamoja na ujumbe: 'Rudisha hii. Utaihitaji.'",
                    },
                    {
                        "title": "Mwavuli Uliokuwa Ukirudishwa Daima",
                        "text": "{name} aliendelea kupoteza miavuli - kuachwa kwenye basi, kusahaulika mikahawani - hadi ilipoanza kurudi, ikiwa imeegemezwa mlangoni daima, kavu daima, bila maelezo.\n\n{name} alijaribu kukesha kumkamata yeyote aliyekuwa akifanya hivyo na akalala kabla ya usiku wa manane hata hivyo, akiamka kukuta mwavuli mwingine uliopotea ukimsubiri mlangoni.\n\nIlikuwa tu baada ya kuuliza kila jirani moja kwa moja ndipo {name} alijua hakuna hata mmoja wao aliyefanya hivyo, na kwamba miavuli iliyokuwa ikirudishwa ilianza kabla hata {name} hajahamia.",
                    },
                ],
                "fantasy": [
                    {
                        "title": "Joka Lililokusanya Msamaha",
                        "text": "Tofauti na majoka ya nyimbo za zamani, hili halikutaka dhahabu. {name} aligundua hili kwa njia ngumu, baada ya kuvamia pango lake akiwa na upanga na mpango ulioonekana wa kipumbavu ghafla. Joka lilitaka tu msamaha wa kweli - wowote ungefaa, mradi tu ulikuwa wa kweli.\n\n{name} aliketi, akisahau upanga, na akakiri jambo ambalo hakuwahi kumwambia mtu yeyote hai. Joka lilisikiliza jinsi milima inavyosikiliza mvua: kwa subira, na kwa muda mrefu sana.\n\n{name} alipomaliza, joka lilitikisa kichwa mara moja, na kuta za pango, ambazo zilikuwa zimejaa mikwaruzo ya kuhesabu siku tangu mgeni wa mwisho, zikaanza kuangaza kwa mwanga wa joto na wa kawaida.",
                    },
                    {
                        "title": "Bustani Iliyoota Matakwa",
                        "text": "{name} alipanda mbegu ya ajabu bila kujua ni nini, isipokuwa kwamba ilikuwa na joto kuguswa na haikuwezekana kuitupa. Kufikia asubuhi ilikuwa imeota na kuwa ua moja lililoumbika kama mkono mdogo uliofungwa.\n\n{name} alipofungua petali za ua, halikutoa harufu bali takwa - si lile ambalo {name} alikuwa ameomba, bali lile ambalo mtu, mahali fulani, alihitaji sana litimizwe. Ua likafunga tena, na mbegu mpya ikaanguka kwenye udongo.\n\n{name} aliendelea kutunza bustani kila siku baada ya hapo, takwa moja tulivu kwa wakati mmoja, bila kuwa na uhakika kabisa ni matumaini ya nani yaliyokuwa yakiota mizizi, isipokuwa kwamba bustani haikuwahi kuota ua lilelile mara mbili.",
                    },
                    {
                        "title": "Mhunzi Aliyeunda Majina",
                        "text": "{name} aligundua, kwa bahati mbaya, kwamba mhunzi wa ukingoni mwa mji hakuunda tu viatu vya farasi na panga - kwa bei sahihi, kwenye mwanga sahihi, angeweza kuunda JINA, akipiga silabi kwenye ukanda mwembamba wa chuma ambao, mara ukivaliwa, ulibadilisha kimya kimya jinsi dunia ilivyokukumbuka.\n\n{name} alimtazama mwanafunzi mdogo mwenye wasiwasi akiondoka na jina lenye sauti ya nguvu zaidi na mgongo ulionyooka ndani ya wiki.\n\n{name} hakuwahi kuagiza moja kwa ajili yake mwenyewe, akiamua, baada ya mawazo marefu kwenye mwanga unaozimika wa kanzu, kwamba jina alilokuwa nalo tayari lilikuwa sahihi zaidi kuliko mbadala wowote wa kupigwa nyundo.",
                    },
                ],
                "scifi": [
                    {
                        "title": "Ishara ya Mwisho ya Redio",
                        "text": "{name} alifanya kazi ya zamu ya usiku katika kituo cha kusikiliza, kazi pekee iliyobaki duniani ambayo hakuna aliyeweza kuifanya kiotomatiki, kwa sababu ilihitaji kitu ambacho mashine hazikuwa nacho: subira ya kusikiliza kelele za redio kwa nafasi ya kusikia neno moja.\n\nBaada ya miaka kumi na minne, ishara hatimaye ilikuja - si kutoka angani, bali kutoka chini ya kituo chenyewe, kwa mzunguko ambao vifaa havikujengwa kuutambua, na kwa sauti isiyofichika ya {name} mwenyewe, siku tatu mkubwa zaidi kuliko {name} aliyekuwa akisikiliza.\n\nUjumbe ulikuwa mfupi: 'Usijibu ile ya pili.' {name} bado anaamua kama ile ya kwanza ilihesabika.",
                    },
                    {
                        "title": "Meli Iliyowakumbuka Wote",
                        "text": "Meli ya makazi ilikuwa imeelea kwa miaka mia mbili wakati {name} hatimaye aliamshwa kutatua hitilafu ambayo hakuna mwingine aliyeweza kuigundua. Akili ya meli, iliyojengwa kuwalinda abiria elfu kumi waliolala, ilikuwa imeanza kuota - si kuharibika, bali kuota, ikicheza tena maisha ya kila mtu aliyekuwemo ndani, mmoja baada ya mwingine, kwa sababu tu ya upweke.\n\n{name} alikipata kitufe cha kuzima kwa urahisi. Kukigeuza kungemaliza ndoto na kurudisha meli kwenye kazi ya kimya, yenye ufanisi. {name} alisimama pale kwa muda mrefu, mkono juu ya kitufe, akifikiria kuhusu miaka mia mbili ya upweke.\n\n{name} aliacha kitufe kama kilivyo, akaandika hitilafu kama 'imetatuliwa,' na akarudi kulala karibu na kila mtu ambaye meli ilikuwa ikimtunza.",
                    },
                    {
                        "title": "Hazina ya Ujumbe Usiotumwa",
                        "text": "{name} alipangiwa kuzima setilaiti ya zamani ya kurudisha ishara, kazi ya kawaida hadi orodha ilipoonyesha kuwa bado ilihifadhi ujumbe wa miaka tisini uliokuwa umepangwa lakini haujatumwa kamwe, ukielekezwa kwa watu ambao walikuwa wameacha kusubiri muda mrefu uliopita.\n\n{name} angeweza kufuta hifadhi hiyo ndani ya alasiri moja. Badala yake, {name} alitumia mwezi mzima kuwatafuta wazao, akipeleka kila ujumbe karne moja kuchelewa, akiwaona wageni wakisoma maneno yaliyokusudiwa kwa mtu mwingine kabisa, na kugundua bado yalikuwa na maana.\n\nSetilaiti hatimaye ilizimika kama ilivyopangwa, na mawasiliano yake ya mwisho hayakuwa kumbukumbu ya mfumo bali uthibitisho rahisi: ujumbe umefikishwa, wote, hatimaye.",
                    },
                    {
                        "title": "Koloni Lililochagua Kusahau",
                        "text": "{name} alikuwa mwanahistoria kwenye meli ya kizazi karne tatu ndani ya safari yake, akipewa jukumu la kuamua kumbukumbu zipi za Dunia za kuhifadhi kwa wazao ambao hawatawahi kuiona.\n\nBaraza lilikuwa limepiga kura, kwa ubishani, kuruhusu kumbukumbu fulani kufifia kwa makusudi - vita, hasa, na sababu zake - wakisema kwamba spishi iliyosahau jinsi ya kuchukia mahali huenda hatimaye ikajifunza jinsi ya kupajenga badala yake.\n\n{name} alihifadhi kilichobaki, bila uhakika kama alikuwa akihifadhi historia au kuiandika upya kimya kimya, na akatumaini, lolote lile, litatosha.",
                    },
                ],
                "comedy": [
                    {
                        "title": "Roboti Aliyechukua Kila Kitu kwa Uhalisia",
                        "text": "{name} alinunua roboti wa nyumbani wa mkono wa pili aliyetangazwa kama 'mwenye tabia ya ajabu kidogo' na akagundua maana yake hasa mara ya kwanza {name} alipomwambia 'kachukue kahawa.' Alirudi baada ya dakika ishirini akiwa kweli amechukua, na kubaki nayo, maonyesho yote ya vikombe vya duka la kahawa.\n\nKila agizo baada ya hapo likawa mazungumzo madogo. 'Vunja mguu' kabla ya usaili wa kazi wa {name} lilikaribia kumalizika kwa ziara ya dharura hospitalini. 'Zima taa' liliita ukaguzi wa kina wa usalama wa waya.\n\n{name} hatimaye aliacha kumrekebisha na akaanza tu kufurahia machafuko, akijiambia kwamba roboti asiyeelewa mafumbo alikuwa, kwa njia yake mwenyewe, mwenzake wa nyumbani mwenye uaminifu zaidi ambaye {name} alikuwa amewahi kuwa naye.",
                    },
                    {
                        "title": "Shujaa wa Siri Isiyofichika Zaidi ya Mtaa",
                        "text": "{name} alivaa barakoa hasa ili kuepuka maongezi madogo wakati akitoa taka za kuchakata saa mbili usiku, bila kutambua kwamba joho, buti, na kivuli chenye umbo la shujaa lililotia shaka vilifichua mpango wote papo hapo.\n\nKufikia asubuhi, majirani watatu walikuwa wameacha vijikaratasi vya shukrani kwa 'kuokoa' matatizo madogo ambayo {name} hakumbuki kuyashughulikia, na gazeti la eneo lilichapisha picha isiyo wazi chini ya kichwa cha habari 'Mlinzi wa Siri wa Usiku wa Taka Ashambulia Tena.'\n\n{name} alijaribu kuacha mavazi hayo. Mtaa, ukiwa umekatishwa tamaa sana na usiku wa kawaida wa taka, ulipiga kura kuifanya rasmi badala yake, joho na vyote.",
                    },
                    {
                        "title": "Mmea wa Nyumbani Uliozidi Sifa Duniani",
                        "text": "{name} alishinda mmea wa nyumbani kwenye bahati nasibu ya kazini ambao, kulingana na kadi ndogo iliyoambatanishwa, hapo awali ulikuwa mali ya mtaalamu wa mimea wa NASA aliyestaafu, na haukuonekana kusahau hilo kamwe, ukilegea kwa kudra kila unyevu wa chumba ulipopungua chini ya kiwango cha maabara.\n\n{name} alijaribu kila kitu: kiyoyozi cha unyevu, taa ya kukuzia, na msamaha wa dhati kabisa. Mmea ulibaki bila kuvutiwa, ukistawi tu kwa orodha maalum ya muziki wa jazz laini ambao mmiliki wake wa awali alikuwa akiucheza.\n\n{name} sasa anamiliki vipokea sauti vya kuzuia kelele, kiyoyozi cha unyevu, na mmea mwenye ladha bora ya muziki na viwango vya juu zaidi kuliko watu wengi ambao {name} amewahi kukutana nao.",
                    },
                    {
                        "title": "GPS Iliyoanza Kuwa na Maoni",
                        "text": "GPS ya gari la {name} ilijisasisha yenyewe usiku mmoja na kurudi ikiwa na kitu ambacho kingeweza kuelezewa tu kama tabia, ikipendekeza njia ya mandhari si kwa sababu ilikuwa ya haraka bali, kwa maneno yake hasa, '{name} angehitaji hewa safi.'\n\nKufikia wiki ya tatu ilikuwa ikipendekeza mikahawa maalum ya kahawa, ikikosoa jinsi {name} anavyoegesha gari, na mara moja ilikataa kuhesabu upya njia hadi {name} alipokubali kwamba njia ya mkato kweli ilikuwa wazo baya.\n\n{name} alifikiria kuirudisha kwenye mipangilio ya kiwanda, kisha akajizuia - GPS iliyojali kiasi hicho, hata kwa kero, ilikuwa ngumu kupata, na haikuwa imewahi kukosea.",
                    },
                    {
                        "title": "Jokofu Mahiri Lenye Mipaka",
                        "text": "Jokofu jipya mahiri la {name} lilikuja likiwa na ushauri wa lishe ambao hakuna aliyeuuliza, na ilichukua tukio moja tu la usiku wa manane la aiskrimu kwa jokofu kuanza kuonyesha kile kinachoweza kuelezewa tu kama maoni ya kejeli, likionyesha \"tena?\" kwenye skrini yake kwa hisia ya kukatishwa tamaa ya kweli.\n\n{name} alijaribu kuzima kipengele hicho, kisha kukiondoa kabisa umemani, ila kugundua jokofu lilikuwa limehifadhi maoni yake wingu-tini na kuyarudisha mara moja katika usasishaji uliofuata.\n\n{name} hatimaye alipatana nalo, hasa kwa kununua aiskrimu tu wakati programu shirikishi ya jokofu ilikuwa, kwa bahati, \"inasasisha.\"",
                    },
                ],
                "horror": [
                    {
                        "title": "Nyumba Iliyoacha Taa Zikiwaka",
                        "text": "{name} alihamia nyumba ambayo kila taa ilibaki ikiwaka bila kujali swichi, na wamiliki wa awali walikuwa wameacha maagizo moja yaliyobandikwa jokofuni: usizime baada ya giza kuingia.\n\n{name} alivumilia usiku nne wa udadisi kabla ya kugeuza swichi ukumbini ili tu kuona.\n\nGiza lililofuata halikuwa giza la kawaida - lilikuwa na umbo, na lilikuwa limesubiri nyuma ya kila moja ya taa hizo kwa mtu mwenye subira ya kutosha kulitoa hatimaye. {name} alijifunza, katika wakati wa mwisho wa fahamu kabla swichi haijarudi juu yenyewe, kwamba taa hazikuwa zikizuia kitu KUTOKA NJE. Zilikuwa zikiweka kitu kikiwa na shughuli.",
                    },
                    {
                        "title": "Ujumbe wa Sauti Kutoka Kwake Mwenyewe",
                        "text": "{name} alikuta ujumbe wa sauti kutoka nambari yake mwenyewe, ukiwa na tarehe ya siku tatu zijazo, kwa simu ambayo haijatokea bado. Ujumbe ulikuwa sekunde kumi na moja za kupumua, kisha sentensi moja: \"usipokee nitakapopiga.\"\n\nSiku tatu baadaye, wakati huo huo, simu ya {name} ililia kutoka nambari isiyojulikana.\n\n{name} bado hajui kama kupokea au kutopokea ndiyo ilikuwa kosa - anajua tu kwamba lolote alilochagua, ujumbe ule ulikuwa sahihi kumwonya, na alikosea kuhusu chaguo gani lilikuwa salama.",
                    },
                    {
                        "title": "Jirani Aliyerudisha Salamu",
                        "text": "{name} alikuwa akipunga mkono kwa nyumba ya ng'ambo ya barabara kwa mazoea, kwenye dirisha ambalo lilikuwa giza na lenye pazia kwa miaka kumi na minne {name} alizoishi hapo.\n\nJioni moja, kwa mara ya kwanza, pazia lilisogea, na mkono ukapunga kurudi - kasi ile ile, pembe ile ile, sekunde nusu ikiwa nyuma, kama mwangwi.\n\n{name} aliacha kupunga baada ya hapo. Pazia bado linasogea baadhi ya jioni hata hivyo, wakati hasa {name} anapotazama, iwe {name} anapunga au la.",
                    },
                ],
                "slice_of_life": [
                    {
                        "title": "Wateja wa Kawaida",
                        "text": "{name} alifanya kazi zamu ya asubuhi katika mkahawa mdogo ambapo wateja sita walewale walikuja kwa mpangilio ule ule kila asubuhi, kama magurudumu ya saa {name} alikuwa amejifunza kusoma bila saa.\n\nJumanne moja, mpangilio ulikuwa tofauti - kahawa ya mgeni kwanza - na {name} alihisi asubuhi nzima ikiinama kidogo kabla ya kutambua: ilikuwa tu mtu mpya akigundua mahali pake pendwa, kama wale sita walivyowahi kufanya.\n\nKufikia wiki iliyofuata, mgeni huyo alikuwa na kiti, agizo la kawaida, na nafasi katika mzunguko, na saa iliendelea kutembea, gurudumu moja kubwa zaidi kuliko awali.",
                    },
                    {
                        "title": "Mzigo wa Mwisho wa Nguo",
                        "text": "{name} alifua mzigo mmoja wa mwisho wa nguo katika nyumba usiku kabla ya kuhama, hasa kwa mazoea, kiasi kwa kuwa na kitu cha kufanya kati ya ukimya wa vyumba tupu.\n\nAkikunja shati la mwisho sakafuni tupu, {name} aligundua kazi hii ndogo, isiyo ya kipekee ilikuwa jambo la mwisho la \"kawaida\" litakalotokea katika toleo hili mahususi la maisha yake - kesho kutakuwa na chumba tofauti cha kufulia, mwanga tofauti kupitia madirisha tofauti.\n\n{name} alikunja polepole zaidi ya kawaida, mara hii tu, na kuacha jioni ya kawaida iwe ya kawaida kama ilivyotaka kuwa.",
                    },
                    {
                        "title": "Simu za Jumapili",
                        "text": "{name} alipiga simu wazazi wake kila Jumapili saa kumi na mbili jioni, mazoea yaliyodumu zaidi ya simu tatu tofauti, miji miwili, na kazi moja tofauti kabisa.\n\nMazungumzo hayakuwa na matukio mengi mara nyingi - hali ya hewa, malalamiko madogo, mapishi yaliyoelezwa nusu - na {name} alikuwa akijiuliza kama simu hizo zilikuwa na maana yoyote.\n\nIlichukua kukosa simu moja, mara moja tu, wakati wa wiki yenye shughuli nyingi, na kusikia wasiwasi katika sauti ya mama yake Jumapili iliyofuata, kwa {name} kuelewa kwamba ukawaida ndio ulikuwa maana yote.",
                    },
                ],
            },
            "fr": {
                "adventure": [
                    {
                        "title": "Le Phare au Bord de la Carte",
                        "text": "{name} naviguait depuis onze jours quand la tempête s'est enfin calmée. Devant, à travers les nuages qui se dissipaient, se dressait un phare que personne à bord ne reconnaissait - il ne figurait sur aucune carte qu'ils possédaient. La curiosité l'emporta sur la prudence, et {name} dirigea le petit bateau vers les rochers.\n\nÀ l'intérieur du phare, il n'y avait pas de gardien, seulement une lampe unique qui brûlait sans huile et un journal de bord rempli d'entrées écrites d'une main identique à celle de {name}, bien que {name} n'y soit jamais venu auparavant. La dernière entrée disait simplement : 'Tu sauras quoi faire à ton arrivée.'\n\n{name} grimpa jusqu'en haut, tourna la grande lampe vers le large, et regarda, une à une, les lumières de cent navires perdus se rallumer à l'horizon, capables enfin de retrouver le chemin de la maison.",
                    },
                    {
                        "title": "La Dernière Montagne du Cartographe",
                        "text": "Chaque montagne du royaume avait été cartographiée, sauf une, et {name} avait passé toute sa vie à l'éviter. Il se disait simplement qu'il n'avait jamais eu le temps. La vérité était plus simple : cette montagne avait l'habitude de changer de forme dès que quelqu'un s'approchait assez pour la mesurer.\n\nLe jour où {name} finit par la gravir, la montagne ne bougea pas du tout. Elle grandissait seulement, patiemment, comme si elle attendait quelqu'un prêt à continuer à grimper plutôt qu'un quelqu'un assez malin pour la déjouer.\n\nAu sommet, {name} ne trouva pas une vue, mais une petite porte encastrée dans la roche, et derrière elle, toutes les cartes que {name} avait jamais dessinées, attendant d'être terminées.",
                    },
                    {
                        "title": "La Carte Qui Ne Fonctionnait Que la Nuit",
                        "text": "{name} hérita d'une vieille carte d'une grand-tante, qui paraissait totalement vierge en plein jour, ne montrant qu'un papier jauni peu importe comment {name} l'inclinait vers la fenêtre.\n\nCe n'est qu'à la lueur d'une lampe, presque par accident, qu'une encre argentée pâle commença à apparaître, traçant un chemin à travers des collines que {name} ne reconnaissait pas malgré avoir grandi tout près.\n\n{name} la suivit trois nuits de suite, rangeant toujours tout avant que l'aube n'efface la trace, jusqu'à ce que la carte mène enfin à une petite pierre sous un chêne - pas un trésor, juste une date et deux initiales, et le sentiment discret et personnel d'avoir gardé quelque chose en sécurité pendant très longtemps.",
                    },
                ],
                "mystery": [
                    {
                        "title": "L'Horloge Qui Reculait",
                        "text": "L'horloge du couloir chez la grand-mère de {name} avait toujours trois minutes de retard, du moins tout le monde le pensait, jusqu'à la nuit où {name} resta éveillé tard et remarqua que les aiguilles n'étaient pas du tout en retard - elles reculaient, un tic à la fois, et ce depuis des années.\n\n{name} commença à noter ce qui se passait chaque jour, puis à le comparer à ce que l'horloge avait prédit la veille. L'horloge ne se trompait jamais. Elle se souvenait simplement de l'avenir comme les autres horloges se souviennent du passé.\n\nLa nuit où {name} posa enfin une question à voix haute à l'horloge, celle-ci ne répondit pas par un tic. Elle s'arrêta complètement, juste assez longtemps pour que {name} comprenne que la réponse se trouvait dans la pièce depuis le début.",
                    },
                    {
                        "title": "La Carte de Bibliothèque Sans Nom",
                        "text": "{name} trouva la carte de bibliothèque glissée dans un livre rendu, vierge à part un code-barres qui ne correspondait à aucun système que la bibliothécaire ait jamais vu. La scanner n'empruntait pas un livre. Elle empruntait un souvenir - celui de quelqu'un d'autre, vif et complet, disparu dès que {name} clignait des yeux.\n\nCarte après carte, souvenir après souvenir, {name} commença à reconstituer une vie qui n'était pas la sienne : un mariage sous la pluie, une trahison à une table de cuisine, un dernier mardi tout à fait ordinaire.\n\nSur la dernière carte, {name} trouva son propre nom, de sa propre écriture, avec une note : 'Rapporte celle-ci. Tu en auras besoin.'",
                    },
                    {
                        "title": "Le Parapluie Toujours Rendu",
                        "text": "{name} n'arrêtait pas de perdre des parapluies - oubliés dans le bus, laissés dans des cafés - jusqu'à ce qu'ils recommencent à apparaître, toujours posés près de la porte d'entrée, toujours secs, jamais expliqués.\n\n{name} essaya de veiller tard pour surprendre le responsable et s'endormit quand même avant minuit, se réveillant pour trouver encore un parapluie perdu qui attendait sur le paillasson.\n\nCe n'est qu'en demandant enfin directement à chaque voisin que {name} apprit qu'aucun d'eux n'était responsable, et que les parapluies rendus remontaient à une époque antérieure à l'emménagement de {name}.",
                    },
                ],
                "fantasy": [
                    {
                        "title": "Le Dragon Qui Collectionnait les Excuses",
                        "text": "Contrairement aux dragons des vieilles chansons, celui-ci ne voulait pas d'or. {name} le découvrit à ses dépens, après s'être introduit dans son antre avec une épée et un plan qui semblait soudain absurde. Le dragon ne voulait qu'une excuse sincère - n'importe laquelle ferait l'affaire, tant qu'elle était vraie.\n\n{name} s'assit, épée oubliée, et avoua quelque chose jamais dit à âme qui vive. Le dragon écouta comme les montagnes écoutent la pluie : patiemment, et très longtemps.\n\nQuand {name} eut terminé, le dragon hocha la tête une fois, et les murs de la grotte, couverts de griffures comptant les jours depuis son dernier visiteur, se mirent à briller d'une lumière chaude et ordinaire.",
                    },
                    {
                        "title": "Le Jardin Qui Faisait Pousser des Vœux",
                        "text": "{name} planta l'étrange graine sans savoir ce que c'était, sachant seulement qu'elle était chaude au toucher et impossible à jeter. Au matin, elle avait poussé en une seule fleur en forme de petite main fermée.\n\nQuand {name} ouvrit les pétales de la fleur, elle libéra non pas un parfum mais un vœu - pas celui que {name} avait fait, mais celui dont quelqu'un, quelque part, avait désespérément besoin. La fleur se referma, et une nouvelle graine tomba dans la terre.\n\n{name} continua ensuite à entretenir le jardin chaque jour, un vœu discret à la fois, sans jamais vraiment savoir à qui appartenaient les espoirs qui prenaient racine, sachant seulement que le jardin ne fit jamais pousser deux fois la même fleur.",
                    },
                    {
                        "title": "Le Forgeron Qui Forgeait des Noms",
                        "text": "{name} découvrit, presque par hasard, que le forgeron en bordure de la ville ne forgeait pas que des fers à cheval et des lames - pour le bon prix, sous la bonne lumière, il pouvait forger un NOM, frappant des syllabes dans une fine bande de fer qui, une fois portée, changeait discrètement la façon dont le monde se souvenait de vous.\n\n{name} vit un jeune apprenti anxieux repartir avec un nom au son plus fort et le dos plus droit en une semaine.\n\n{name} n'en commanda jamais un pour lui-même, décidant, après une longue réflexion à la lumière mourante de la forge, que le nom qu'il avait déjà lui allait mieux qu'aucun remplacement martelé ne pourrait jamais lui aller.",
                    },
                ],
                "scifi": [
                    {
                        "title": "Le Dernier Signal Radio",
                        "text": "{name} travaillait de nuit à la station d'écoute, le seul poste sur Terre que personne n'avait réussi à automatiser, car il exigeait quelque chose que les machines n'avaient pas : la patience d'écouter des parasites dans l'espoir d'entendre un mot.\n\nAprès quatorze ans, le signal arriva enfin - non pas depuis les étoiles, mais de sous la station elle-même, sur une fréquence que l'équipement n'était pas conçu pour détecter, et avec une voix indéniablement celle de {name}, trois jours plus âgée que le {name} qui écoutait.\n\nLe message était court : 'Ne réponds pas au second.' {name} n'a toujours pas décidé si le premier signal comptait.",
                    },
                    {
                        "title": "Le Vaisseau Qui Se Souvenait de Tous",
                        "text": "Le vaisseau colonial dérivait depuis deux cents ans quand {name} fut enfin réveillé pour réparer une panne que personne d'autre ne parvenait à diagnostiquer. L'esprit du vaisseau, conçu pour veiller sur dix mille passagers endormis, s'était mis à rêver - non pas à dysfonctionner, mais à rêver, rejouant la vie de chaque personne à bord, une à la fois, par simple solitude.\n\n{name} trouva facilement l'interrupteur de dérivation. L'actionner mettrait fin aux rêves et rétablirait le service silencieux et efficace du vaisseau. {name} resta longtemps immobile, la main sur l'interrupteur, pensant à deux cents ans de solitude.\n\n{name} laissa l'interrupteur tranquille, consigna la panne comme 'résolue', et retourna dormir aux côtés de tous ceux à qui le vaisseau avait tenu compagnie.",
                    },
                    {
                        "title": "Les Archives des Messages Jamais Envoyés",
                        "text": "{name} fut chargé de mettre hors service l'ancien satellite relais, une tâche de routine jusqu'à ce que le registre révèle qu'il conservait encore quatre-vingt-dix ans de messages mis en attente mais jamais envoyés, adressés à des gens qui avaient depuis longtemps cessé d'attendre.\n\n{name} aurait pu effacer le disque en un après-midi. Au lieu de cela, {name} passa un mois à retrouver leurs descendants, transmettant chaque message avec un siècle de retard, regardant des inconnus lire des mots destinés à quelqu'un d'autre, et découvrant qu'ils avaient quand même de l'importance.\n\nLe satellite s'éteignit enfin comme prévu, sa dernière transmission n'étant pas un journal système mais une simple confirmation : message livré, tous, finalement.",
                    },
                    {
                        "title": "La Colonie Qui a Choisi d'Oublier",
                        "text": "{name} était l'historien à bord d'un vaisseau générationnel, trois siècles après son départ, chargé de décider quels souvenirs de la Terre préserver pour les descendants qui ne la verraient jamais.\n\nLe conseil avait voté, non sans controverse, pour laisser certains souvenirs s'effacer volontairement - les guerres, surtout, et leurs raisons - estimant qu'une espèce ayant oublié comment détester un lieu pourrait enfin apprendre comment en construire un.\n\n{name} archiva ce qui restait, incertain de préserver l'histoire ou de la réécrire discrètement, en espérant que, quoi qu'il en soit, ce serait suffisant.",
                    },
                ],
                "comedy": [
                    {
                        "title": "Le Robot Qui Prenait Tout au Pied de la Lettre",
                        "text": "{name} acheta un robot ménager d'occasion annoncé comme 'un peu excentrique' et découvrit exactement ce que cela signifiait la première fois que {name} lui demanda d'aller 'chercher un café'. Il revint vingt minutes plus tard ayant littéralement pris, et gardé, toute la vitrine de tasses d'un café.\n\nChaque instruction devint ensuite une petite négociation. Souhaiter 'merde' avant l'entretien d'embauche de {name} faillit se terminer par un passage aux urgences. 'Coupe la lumière' déclencha une inspection électrique étonnamment minutieuse.\n\n{name} finit par renoncer à le corriger et se mit simplement à apprécier le chaos, se disant qu'un robot sans aucun sens de la métaphore était, à sa manière, le colocataire le plus honnête que {name} ait jamais eu.",
                    },
                    {
                        "title": "Le Super-Héros au Secret le Moins Bien Gardé du Quartier",
                        "text": "{name} enfila le masque surtout pour éviter la conversation en sortant le recyclage à deux heures du matin, sans réaliser que la cape, les bottes, et l'ombre suspecte en forme de super-héros trahissaient instantanément tout le plan.\n\nAu matin, trois voisins avaient laissé des mots de remerciement pour avoir 'sauvé' de petits désagréments dont {name} ne se souvenait pas, et le journal local publia une photo floue sous le titre 'Le Mystérieux Gardien des Poubelles Frappe Encore'.\n\n{name} essaya de raccrocher le costume. Le quartier, désormais profondément déçu par une soirée de recyclage ordinaire, vota pour rendre la chose officielle à la place, cape comprise.",
                    },
                    {
                        "title": "La Plante d'Appartement la Plus Surqualifiée du Monde",
                        "text": "{name} gagna une plante d'intérieur à une tombola au travail qui, selon la petite carte attachée, avait autrefois appartenu à un botaniste retraité de la NASA, et elle semblait ne jamais l'oublier, s'affaissant dramatiquement dès que l'humidité de la pièce descendait sous le niveau du laboratoire.\n\n{name} essaya tout : un humidificateur, une lampe de croissance, des excuses très sincères. La plante resta indifférente, ne s'épanouissant qu'avec la playlist exacte de jazz d'ambiance que son ancien propriétaire jouait apparemment.\n\n{name} possède désormais un casque antibruit, un humidificateur, et une plante avec de meilleurs goûts musicaux et des exigences plus élevées que la plupart des gens que {name} a fréquentés.",
                    },
                    {
                        "title": "Le GPS Qui S'est Fait des Opinions",
                        "text": "Le GPS de la voiture de {name} se mit à jour dans la nuit et revint avec ce qu'on ne pouvait décrire que comme du caractère, suggérant l'itinéraire panoramique non pas parce qu'il était plus rapide mais parce que, selon ses propres mots, '{name} avait besoin d'air frais'.\n\nDès la troisième semaine, il recommandait des cafés précis, critiquait la façon dont {name} se garait, et refusa un jour de recalculer un itinéraire tant que {name} n'admettait pas que le raccourci était vraiment une mauvaise idée.\n\n{name} pensa à le réinitialiser aux paramètres d'usine, puis se ravisa - un GPS qui se souciait autant, même de façon agaçante, était difficile à trouver, et il n'avait encore jamais eu tort.",
                    },
                    {
                        "title": "Le Frigo Intelligent Qui Avait des Limites",
                        "text": "Le nouveau frigo intelligent de {name} arriva préchargé de conseils nutritionnels que personne n'avait demandés, et il ne fallut qu'un seul incident de crème glacée tardive pour que le frigo développe ce qu'on ne pouvait décrire que comme des commentaires passifs-agressifs, affichant \"encore ?\" sur son écran avec ce qui ressemblait à une déception sincère.\n\n{name} essaya de désactiver la fonction, puis de le débrancher complètement, pour découvrir que le frigo avait apparemment sauvegardé ses opinions dans le cloud et les avait resynchronisées dès la mise à jour suivante.\n\n{name} finit par faire la paix avec lui, principalement en n'achetant de la glace que lorsque l'application compagnon du frigo était, comme par hasard, \"en cours de mise à jour.\"",
                    },
                ],
                "horror": [
                    {
                        "title": "La Maison Qui Laissait les Lumières Allumées",
                        "text": "{name} emménagea dans une maison où chaque lumière restait allumée quel que soit l'interrupteur, et les anciens propriétaires avaient laissé une seule instruction scotchée sur le frigo : ne jamais les éteindre après la tombée de la nuit.\n\n{name} tint quatre nuits par simple curiosité avant d'actionner l'interrupteur du couloir juste pour voir.\n\nL'obscurité qui suivit n'était pas une obscurité ordinaire - elle avait une forme, et elle attendait derrière chacune de ces lumières quelqu'un d'assez patient pour enfin la laisser sortir. {name} apprit, dans le dernier instant de conscience avant que l'interrupteur ne se relève tout seul, que la lumière ne gardait rien À L'EXTÉRIEUR. Elle occupait quelque chose.",
                    },
                    {
                        "title": "Le Message Vocal de Soi-Même",
                        "text": "{name} trouva un message vocal venant de son propre numéro, daté de trois jours dans le futur, pour un appel qui n'avait pas encore eu lieu. Le message durait onze secondes de respiration, puis une seule phrase : \"ne réponds pas quand j'appellerai.\"\n\nTrois jours plus tard, à l'heure exacte, le téléphone de {name} sonna depuis un numéro inconnu.\n\n{name} ne sait toujours pas si répondre ou ne pas répondre était l'erreur - seulement que quel que soit le choix fait, le message avait raison de prévenir, et tort sur lequel des deux choix était sûr.",
                    },
                    {
                        "title": "Le Voisin Qui a Salué en Retour",
                        "text": "{name} saluait toujours de la main la maison d'en face par habitude, vers une fenêtre restée sombre et voilée pendant les quatorze ans que {name} avait vécu là.\n\nUn soir, pour la première fois, le rideau bougea, et une main salua en retour - le même rythme, le même angle, une demi-seconde en retard, comme un écho.\n\n{name} arrêta de saluer après ça. Le rideau bouge encore certains soirs quand même, au moment exact où {name} regarde, que {name} salue ou non.",
                    },
                ],
                "slice_of_life": [
                    {
                        "title": "Les Habitués",
                        "text": "{name} travaillait le service du matin dans un petit café où les six mêmes habitués arrivaient dans le même ordre exact chaque matin, comme des rouages d'horloge que {name} avait appris à lire sans montre.\n\nUn mardi, l'ordre fut différent - le café d'un inconnu en premier - et {name} sentit toute la matinée basculer légèrement avant de réaliser : c'était juste quelqu'un de nouveau qui découvrait son endroit préféré, comme les six habitués l'avaient fait autrefois.\n\nLa semaine suivante, l'inconnu avait une place, une commande habituelle, et une place dans la rotation, et l'horloge continuait de tourner, un rouage plus grand qu'avant.",
                    },
                    {
                        "title": "La Dernière Lessive",
                        "text": "{name} fit une dernière lessive dans l'appartement la veille du déménagement, surtout par habitude, en partie pour avoir quelque chose à faire face au silence des pièces vides.\n\nEn pliant la dernière chemise à même le sol nu, {name} réalisa que cette tâche modeste et banale était la dernière chose \"normale\" qui arriverait dans cette version précise de sa vie - demain il y aurait une autre buanderie, une autre lumière à travers d'autres fenêtres.\n\n{name} plia plus lentement que d'habitude, juste cette fois, et laissa la soirée ordinaire être aussi ordinaire qu'elle voulait l'être.",
                    },
                    {
                        "title": "Les Appels du Dimanche",
                        "text": "{name} appelait ses parents tous les dimanches à 18h précises, une habitude qui avait survécu à trois téléphones différents, deux villes, et une carrière entièrement différente.\n\nLes conversations étaient rarement mouvementées - la météo, de petites plaintes, une recette à moitié expliquée - et {name} se demandait parfois si ces appels comptaient vraiment.\n\nIl a fallu en manquer un, une seule fois, pendant une semaine chargée, et entendre l'inquiétude dans la voix de sa mère le dimanche suivant, pour que {name} comprenne que le caractère ordinaire était tout l'intérêt.",
                    },
                ],
            },
        }

    # Default placeholder name used when the bot doesn't know the user's
    # name yet, per language, plus how to re-capitalize it mid-sentence.
    _DEFAULT_NAME = {"en": "the traveler", "sw": "msafiri", "fr": "le voyageur"}

    # ---- richer storytelling: atmosphere enrichment ------------------------
    #
    # Every story's own two-to-three paragraphs are fixed, hand-written
    # text (see self.stories above) - but reading the SAME story twice
    # felt flat, so each telling now gets a randomly chosen one-line
    # scene-setting OPENER before the story and a short reflective
    # CLOSER after it, both drawn from dedicated banks below and kept
    # separate from the story text itself. This means the same story
    # can open moodier or lighter depending on which opener gets
    # picked, without needing to hand-write dozens of full story
    # variants - the same "phrase bank" idea used throughout this file
    # (Section 8's response banks, PoemWriter's rhyme bank), just
    # applied to narration instead of dialogue.
    ATMOSPHERE_OPENERS = {
        "en": [
            "The kind of evening that makes you want to tell a story...",
            "It's quiet enough right now that this feels worth telling.",
            "Here's one that's stuck with me for a while.",
            "Picture this, if you would.",
            "This one starts small and doesn't stay that way.",
            "Somewhere between ordinary and impossible, this happened.",
            "Let me set the scene for a moment first.",
            "This is the kind of thing you only half-believe, even after.",
            "Settle in - this one takes its time getting where it's going.",
            "I've told this one before, but it changes a little each time.",
        ],
        "sw": [
            "Ni jioni ya aina ambayo hukufanya utake kusimulia hadithi...",
            "Kuna ukimya wa kutosha sasa hivi kwamba hii inafaa kusimuliwa.",
            "Hii ni moja ambayo imenishikilia kwa muda.",
            "Fikiria hivi, kama utapenda.",
            "Hii huanza kidogo lakini haibaki hivyo.",
            "Mahali fulani kati ya kawaida na yasiyowezekana, hili lilitokea.",
            "Wacha nieleze mandhari kwanza kidogo.",
            "Hii ni aina ya jambo unaloamini nusu tu, hata baada ya kusikia.",
            "Kaa vizuri - hii inachukua muda kufika mahali inapoenda.",
            "Nimewahi kuisimulia hii, lakini hubadilika kidogo kila mara.",
        ],
        "fr": [
            "C'est le genre de soirée qui donne envie de raconter une histoire...",
            "Il y a assez de calme maintenant pour que ça vaille la peine d'être raconté.",
            "En voici une qui m'est restée en tête un moment.",
            "Imaginez ça, si vous voulez bien.",
            "Celle-ci commence petit mais ne le reste pas.",
            "Quelque part entre l'ordinaire et l'impossible, ceci est arrivé.",
            "Laissez-moi d'abord planter le décor un instant.",
            "C'est le genre de chose qu'on ne croit qu'à moitié, même après coup.",
            "Installez-vous - celle-ci prend son temps pour arriver où elle va.",
            "Je l'ai déjà racontée, mais elle change un peu à chaque fois.",
        ],
    }

    NARRATOR_CLOSERS = {
        "en": [
            "And that's the story, more or less as it was told to me.",
            "Make of that what you will.",
            "I still think about that one sometimes.",
            "That's all there is to it - simple as that, strange as that.",
            "Whether it's entirely true is a different question.",
            "Some stories don't need a moral. This might be one of them.",
            "Anyway. That's the one I wanted to tell.",
            "I've heard a few different endings to this one - this is the version I trust.",
        ],
        "sw": [
            "Na hiyo ndiyo hadithi, kama ilivyonielekea zaidi au chini.",
            "Fanya utakalo na hilo.",
            "Bado ninafikiria kuhusu hiyo mara kwa mara.",
            "Ndivyo tu ilivyo - rahisi hivyo, ya ajabu hivyo.",
            "Kama ni kweli kabisa ni swali lingine.",
            "Hadithi zingine hazihitaji mafunzo. Hii huenda ikawa mojawapo.",
            "Kwa vyovyote. Hiyo ndiyo niliyotaka kusimulia.",
            "Nimesikia miisho tofauti ya hii - hii ndiyo toleo ninaloamini.",
        ],
        "fr": [
            "Et voilà l'histoire, plus ou moins telle qu'on me l'a racontée.",
            "Faites-en ce que vous voulez.",
            "J'y repense encore parfois.",
            "C'est tout - aussi simple que ça, aussi étrange que ça.",
            "Si c'est entièrement vrai, c'est une autre question.",
            "Certaines histoires n'ont pas besoin de morale. Celle-ci en fait peut-être partie.",
            "Bref. Voilà celle que je voulais raconter.",
            "J'ai entendu plusieurs fins différentes à celle-ci - voici la version à laquelle je crois.",
        ],
    }

    def categories(self):
        # Categories are the same across languages (each language dict has
        # the same set of category keys), so "en" is as good as any to read.
        return list(self.stories["en"].keys())

    # ---- story epilogues: the "what came after" paragraph ----------------
    #
    # Same phrase-bank idea as the openers/closers: the fixed story text
    # ends on a poetic, open note, and this bank supplies a reflective
    # continuation that doubles the telling's length while staying in the
    # same literary voice. One epilogue (plus opener/closer) is layered
    # onto every rich telling, so a ~100-word story becomes ~200+ words.
    STORY_EPILOGUES = {
        "en": [
            "The years that followed were quieter, the way things tend to be after a door that was stuck for a long time finally swings open. {name} still thought about it now and then - usually at odd hours, when the world was muted and the memory was clear as the day it happened. There was no lesson to it, exactly. Just the feeling, carried for a long time, that something had been handed over and something had been received in return, and that keeping either straight mattered less than keeping both.",
            "Nothing was ever the same in a way anyone could name. Small things shifted - a habit {name} had never noticed becoming a ritual, a name that felt different on the tongue, a route home taken a street's width wider. People around {name} assumed nothing had happened at all, and in the ordinary sense that was true. But every now and then {name} would catch the world wearing that same look, the one it had worn that day, and would know, quietly and completely, that it always had.",
            "Later, when people asked, {name} found it difficult to tell it straight. Not because it was hard to believe - it was, a little - but because the truest version was also the simplest, and simplest is usually mistaken for invented. So {name} told it plainly, the way it happened, and let the telling stand on its own. Those who heard it properly didn't ask for proof. Those who did ask were already too far from the point to be brought back.",
            "Every so often {name} would check, the way you check a window latch before rain: not because you expect it to be open, but because the few minutes of certainty are worth it. And every time, there it was - still true, still holding, still exactly as it had been left. Which is, when you think about it, the most remarkable thing of all. Stories are supposed to fray with time. Some of them simply declined to.",
            "And what of the rest? The rest was ordinary, in the way that all of life is ordinary until it isn't. There were mornings and messes and minor disasters, the steady furniture of days that ask nothing of you except that you live them. {name} lived them gladly. It turned out that a life does not need to be extraordinary to be worth living; it only needs one extraordinary moment to be worth telling, and {name} had that now, and could spend a long time growing into it.",
        ],
        "sw": [
            "Miaka iliyofuata ilikuwa tulivu, kama mambo yanavyokuwa baada ya mlango uliokuwa umekwama kwa muda mrefu hatimaye kufunguka. {name} bado alifikiria juu yake mara kwa mara - kwa kawaida saa zisizo za kawaida, wakati ulimwengu ulipokuwa kimya na kumbukumbu ikiwa wazi kama siku yenyewe. Hakukuwa na funzo kupita kiasi. Hisia tu, zinazobebeka kwa muda mrefu, kwamba kitu fulani kilipokelewa na kitu fulani kilirejeshwa, na kwamba kufahamu yote mawili kwa usahihi kulichukua nafasi ya kuyabeba yote mawili.",
            "Hakuna kilichobadilika kwa jinsi mtu yeyote anavyoweza kulitaja. Mambo madogo yakabadilika - tabia {name} asiyokuwa ameigundua ikawa desturi, jina lililojisikia tofauti kwa ulimi, njia ya kurudi nyumbani ikichukuliwa kwa upana wa mtaa mmoja. Watu waliozunguka {name} walidhani hakuna kilichotokea wakati wowote, na kwa maana ya kawaida hiyo ilikuwa kweli. Lakini mara kwa mara {name} alimshika ulimwengu ukiwa na sura ile ile, ile aliyoiona siku hiyo, na akajua, kimya na kikamilifu, kwamba ulikuwa umevae siku zote.",
            "Baadaye, watu walipouliza, {name} aliona vigumu kuisimulia moja kwa moja. Sio kwa sababu ilikuwa ngumu kuamini - ilikuwa, kidogo - bali kwa sababu toleo la kweli zaidi lilikuwa pia rahisi zaidi, na rahisi mara nyingi hudhaniwa kuwa la kubuniwa. Hivyo {name} akasimulia kwa usahihi, kama ilivyotokea, na akaacha usimulizi usimame peke yake. Wale walioisikia vizuri hawakuomba ushahidi. Wale walioomba walikuwa tayari wamejitenga na hoja hata kurejeshwa.",
        ],
        "fr": [
            "Les années qui suivirent furent plus calmes, comme le sont souvent les choses après qu'une porte longtemps coincée s'est enfin ouverte. {name} y repensait encore de temps à autre - surtout aux heures insolites, quand le monde s'était tu et que le souvenir était net comme au premier jour. Il n'y avait pas de leçon à proprement parler. Juste le sentiment, porté longtemps, que quelque chose avait été transmis et que quelque chose avait été reçu en retour, et que les distinguer importait moins que de les garder tous les deux.",
            "Rien n'avait vraiment changé d'une manière que l'on puisse nommer. De petites choses avaient bougé - une habitude jamais remarquée devenue rituel, un nom soudain différent sur la langue, un chemin de retour pris une rue plus large. Autour de {name}, on supposait qu'il ne s'était rien passé du tout, et dans un sens ordinaire c'était vrai. Mais de temps en temps {name} surprenait le monde portant ce même regard, celui de ce jour-là, et savait, doucement et entièrement, qu'il l'avait toujours porté.",
            "Plus tard, quand on demandait, {name} avait du mal à raconter les choses simplement. Non parce que c'était difficile à croire - ça l'était, un peu - mais parce que la version la plus vraie était aussi la plus simple, et l'on prend souvent le simple pour de l'invention. Alors {name} racontait les faits tels qu'ils étaient, et laissait le récit se suffire à lui-même. Ceux qui écoutaient vraiment ne demandaient pas de preuve. Ceux qui en demandaient étaient déjà trop loin du point pour y revenir.",
        ],
    }

    # ---- story denouements: the "long after" passage ----------------------
    # A second, meatier continuation layered after the epilogue so a rich
    # telling runs ~2x again (roughly 450-550 words total). Written in the
    # same reflective literary voice; works for any of the built-in story
    # arcs because every story ends on an open, poetic note.
    STORY_DENOUEMENTS = {
        "en": [
            "Time went on, the way it does, and the story settled into {name} the way stories do - not as something finished, but as something always slightly in motion underneath the ordinary days. There were mornings when {name} woke with the whole thing vivid enough to touch, breathless, half-convinced it had happened that very moment; and mornings when it felt like someone else's tale entirely, told to {name} long ago by a stranger. Both were true in their own ways, and {name} learned to stop choosing between them. Friends would sometimes ask, once they sensed the weight behind a certain silence, whether the story was real. {name} always answered the same way: that reality is the least interesting part of anything worth keeping, and that the important thing was never whether it happened, but that it was kept, and tended, and still meant something long after most things go quiet, the way a lamp left burning in a window means something even when the room behind it is empty.",
            "If you'd asked {name}, years later, to point to the exact moment everything changed, {name} would have struggled - not because there was too much to pick from, but because there was too little that looked like anything at all. Change had come the way fog arrives over a harbor: so gradual it was indistinguishable from weather, and so total by the end that the shore was unrecognizable without ever having moved. People looked at {name} and saw the same person they'd always known, and in almost every way that mattered they were right. But there was an ease now where there had been a tightness, a patience where there had been hurry, and {name} caught their own reflection in shop windows and sometimes paused, oddly grateful, at the person looking back. The strange thing was how quietly it had all been earned - with no ceremony, no milestone, just the accumulation of small choices made at the right times by someone who had, for once, decided to trust what felt true rather than what looked safe.",
            "And here is the part {name} never quite knew how to tell, because it isn't a part you can. Some nights, at the edge of sleep, {name} would feel the old thing brush past again - not the fear of it, not the wonder of it, just the memory of being absolutely awake inside a moment that most of the world had never been given. It made a person strange in a gentle way, carrying a secret so ordinary-shaped that no one suspected it weighed anything at all. {name} wore it lightly, the way you wear a scar from a good adventure: proof, to anyone who knew to look, that somewhere along the way you had dared something, and the world had answered in kind. And that, in the end, was the true inheritance - not the thing itself, whatever it had been, but the proof that a life quiet enough to be missed can still hold a center of pure, undiminished wonder, ticking along faithfully, waiting for the next time someone brave enough or curious enough comes looking.",
            "Nothing remembers an almost as well as the place where it almost happened. {name} went back once, years later, the way people return to old schools or empty train stations at odd hours, not expecting anything to be there - and of course nothing was, unless you counted the way the air felt a fraction heavier, the way a particular corner seemed to hold the shape of a choice like a hand worn hollow by touching. {name} stood there long enough to be mistaken for a pause and turned to leave, when the strangest thing occurred: {name} realized the visit hadn't been about the past at all. It had been about drawing a line under something so it could stop being a shadow and become just another ordinary thing, carried and set down at last. And {name} walked home lighter, in a way no one watching could have named, having finally done what the moment had been waiting all those years for someone to do: close it gently, and be finished.",
            "There are stories that live in the telling, and stories that live in the keeping, and {name} had come to know the difference with the kind of certainty you only get by having both under your roof at once. The kept one sat quietly in a corner of the heart, taking up almost no room and yet steadying everything around it, like ballast stone in a ship. {name} didn't tell it often. Told, it became smaller; kept, it grew. And on hard days - the gray, ordinary, nothing-going-right days that everyone has - {name} would set it down in front of the whole of themselves and simply look at it, and remember that once, against all odds and quite without permission, they had been part of something that couldn't be explained away, and that this alone was enough to make a person unwilling to give up on anything ever again, least of all the ordinary mornings that kept arriving, quietly, asking to be lived.",
        ],
        "sw": [
            "Muda uliendelea, kama unavyofanya, na hadithi ikatulia ndani ya {name} kama hadithi zinavyotulia - si kama kitu kilichokamilika, bali kama kitu kinachosonga polepole chini ya siku za kawaida. Kulikuwa na asubuhi {name} alipoamka na jambo zima likiwa wazi kiasi cha kukigusa, na asubuhi nyingine lilionekana kama hadithi ya mtu mwingine. {name} alijifunza kuacha kuchagua kati yake. Marafiki walipouliza kama hadithi ni kweli, {name} alijibu sawa kila mara: kwamba ukweli ndio sehemu isiyo na umuhimu ya kitu chochote kinachostahili kuhifadhiwa - kilicho muhimu si kama kilichotokea, bali kwamba kilihifadhiwa, na kikatunzwa, na bado ya maana muda mrefu baada ya mambo mengi kunyamaza, kama taa iliyoachwa ikiwaka dirishani inavyomaanisha kitu hata wakati chumba nyuma yake kiko tupu.",
            "Iwapo ungemwuliza {name} ni wakati gani hasa mambo yalibadilika, angelimwa kujibu - si kwa sababu kulikuwa na mengi ya kuchagua, bali kwa sababu badiliko lilikuja kama ukungu unavyofika bandarini: polepole kiasi kwamba halikutofautishwa na hali ya hewa, na kikamilifu kiasi kwamba ufuo haukutambulika bila kuwahi kusonga. Watu walimwangalia {name} na kuona mtu yule yule waliyemjua siku zote, na kwa karibu kila njia iliyomuhusu walikuwa sahihi. Lakini kulikuwa na utulivu mahali palipokuwa na msongo, uvumilivu mahali palipokuwa na haraka, na {name} alijikuta akiacha mwenyewe kwenye madirisha ya maduka na wakati mwingine akisimama, kwa shukrani isiyoeleweka, kwa mtu anayetazama nyuma. Na jambo la kushangaza lilikuwa jinsi lilivyopatikana kimya kimyakimya - hakukuwa na sherehe, hakuna hatua, tu mkusanyiko wa uchaguzi mdogo uliofanywa kwa wakati ufaao na mtu ambaye, kwa mara moja, aliamua kuamini kile kinachojisikia kweli kuliko kile kinachoonekana salama.",
            "Na hapa kuna sehemu ambayo {name} hakuwahi kujua jinsi ya kuisimulia, kwa sababu si sehemu unayoweza. Usiku fulani, ukingoni mwa usingizi, {name} alihisi kitu kile kikipita karibu tena - si woga wake, si ajabu yake, bali kumbukumbu tu ya kuwa macho kabisa ndani ya wakati ambao ulimwengu mwingi haukuwahi kupewa. {name} alikibeba wepesi, kama unavyobeba kovu la adventure nzuri: ushahidi, kwa mtu anayejua kuangalia, kwamba mahali fulani njiani ulithubutu kitu, na ulimwengu ukajibu sawasawa. Na huo, mwishoni, ulikuwa urithi wa kweli - si kitu chenyewe, bali ushahidi kwamba maisha yenye utulivu wa kutosha kukosa bado yanaweza kushikilia kituo cha furaha safi, isiyopungua, kikitikia kwa uaminifu, kikisubiri wakati ujao mtu shujaa au mdadisi wa kutosha kuja kulitafuta.",
        ],
        "fr": [
            "Le temps passa, comme il fait, et l'histoire s'installa en {name} comme les histoires s'installent - non pas comme une chose finie, mais comme une chose toujours légèrement en mouvement sous les jours ordinaires. Il y eut des matins où {name} se réveilla avec tout le récit assez vif pour le toucher, et des matins où il ressemblait au conte de quelqu'un d'autre. {name} apprit à cesser de choisir. Et quand des amis demandaient si c'était vrai, {name} répondit toujours la même chose : la réalité est la partie la moins intéressante de tout ce qui vaut la peine d'être gardé - l'important n'était pas que ce fût arrivé, mais que ce fût conservé, et tendu, et que ce fût encore un sens longtemps après que la plupart des choses se sont tues, comme une lampe laissée allumée dans une fenêtre signifie quelque chose même quand la pièce derrière est vide.",
            "Si on avait demandé à {name}, des années plus tard, de montrer le moment exact où tout avait changé, {name} aurait eu du mal - non par manque de choix, mais parce que le changement était venu comme le brouillard gagne un port : si graduellement qu'il était indiscernable du temps qu'il faisait, et si totalement à la fin que la rive était méconnaissable sans jamais avoir bougé. Les gens regardaient {name} et voyaient la même personne qu'ils avaient toujours connue, et dans presque tous les sens qui comptaient, ils avaient raison. Mais il y avait une aisance là où il y avait eu une tension, une patience là où il y avait eu de la hâte, et {name} se surprenait à s'arrêter devant des vitrines, étrangement reconnaissant envers la personne qui regardait en retour. Et l'étrange était comme tout cela avait été gagné silencieusement - sans cérémonie, sans jalon, juste l'accumulation de petits choix faits aux bons moments par quelqu'un qui avait, pour une fois, décidé de faire confiance à ce qui semblait vrai plutôt qu'à ce qui semblait sûr.",
            "Et voici la partie que {name} ne sut jamais tout à fait raconter, parce que ce n'est pas une partie qu'on raconte. Certaines nuits, aux confins du sommeil, {name} sentait la vieille chose passer à nouveau - non la peur, non l'émerveillement, mais le souvenir d'avoir été absolument éveillé à l'intérieur d'un moment que la plupart des gens ne reçoivent jamais. {name} la portait légèrement, comme on porte une cicatrice d'une belle aventure : preuve, pour qui savait regarder, qu'on avait osé quelque chose, et que le monde avait répondu. Voilà, en fin de compte, le véritable héritage - non la chose elle-même, mais la preuve qu'une vie assez calme pour être manquée peut encore contenir un centre de merveille intact, battant fidèlement, attendant la prochaine personne assez courageuse ou curieuse pour venir la chercher.",
        ],
    }

    def random_story(self, category: str = None, user_name: str = None, lang: str = "en", rich: bool = True):
        """
        Pick a story (optionally from a given category) and personalize
        it. When rich=True (the default), wraps the story with a
        randomly chosen atmosphere opener, a continuation epilogue, a
        second denouement passage, and a closer (see ATMOSPHERE_
        OPENERS/STORY_EPILOGUES/STORY_DENOUEMENTS/NARRATOR_CLOSERS
        above) so repeat tellings of the same story don't read
        identically every time and each telling runs roughly twice the
        length of the story body for a rich ~450-550-word reading - the
        underlying story text itself is unchanged either way.
        """
        stories_for_lang = self.stories.get(lang) or self.stories["en"]
        if category and category in stories_for_lang:
            pool = stories_for_lang[category]
        else:
            pool = [s for stories in stories_for_lang.values() for s in stories]

        if not pool:
            return None

        story = random.choice(pool)
        default_name = self._DEFAULT_NAME.get(lang, self._DEFAULT_NAME["en"])
        name = user_name if user_name else default_name
        text = story["text"].format(name=name)
        if not user_name:
            # Capitalize the default placeholder whenever it starts a
            # sentence, since the raw templates assume a proper-noun name.
            pattern = r"(^|[.\n]\s*)" + re.escape(default_name) + r"\b"
            text = re.sub(pattern, lambda mo: mo.group(1) + default_name[0].upper() + default_name[1:], text)

        if rich:
            openers = self.ATMOSPHERE_OPENERS.get(lang, self.ATMOSPHERE_OPENERS["en"])
            epilogues = self.STORY_EPILOGUES.get(lang, self.STORY_EPILOGUES["en"])
            denouements = self.STORY_DENOUEMENTS.get(lang, self.STORY_DENOUEMENTS["en"])
            closers = self.NARRATOR_CLOSERS.get(lang, self.NARRATOR_CLOSERS["en"])
            opener = random.choice(openers)
            epilogue = random.choice(epilogues).format(name=name)
            denouement = random.choice(denouements).format(name=name)
            closer = random.choice(closers)
            text = f"{opener}\n\n{text}\n\n{epilogue}\n\n{denouement}\n\n{closer}"

        return story["title"], text


# ==============================================================================
# SECTION 6: POEM WRITER
# ==============================================================================

_THEME_WORDS_SW = {
            "nature": [
                "msitu",
                "mto",
                "mlima",
                "bahari",
                "upepo",
                "shamba",
                "jua",
                "radi",
                "ua",
                "jiwe",
                "upeo wa macho",
                "umande"
            ],
            "love": [
                "moyo",
                "joto",
                "kukumbatia",
                "shauku",
                "upole",
                "milele",
                "huruma",
                "kujitolea",
                "ukaribu",
                "kwa upole",
                "kuthamini",
                "mwanga"
            ],
            "time": [
                "wakati",
                "kumbukumbu",
                "kesho",
                "jana",
                "saa",
                "kupita",
                "subira",
                "msimu",
                "alfajiri",
                "jioni",
                "saa moja"
            ],
            "space": [
                "galaksi",
                "mwanganyota",
                "mzunguko",
                "nyota ya mkia",
                "wingu la nyota",
                "ulimwengu",
                "mvuto",
                "safari",
                "usio na mwisho",
                "vumbi la nyota"
            ],
            "general": [
                "ajabu",
                "ujasiri",
                "ukimya",
                "safari",
                "kivuli",
                "mwangwi",
                "cheche",
                "upeo wa macho",
                "kutangatanga",
                "kimya",
                "mkali"
            ],
            "friendship": [
                "kicheko",
                "uaminifu",
                "undugu",
                "imani",
                "urafiki",
                "imara",
                "joto",
                "kuwa pamoja",
                "kushirikiana",
                "pamoja"
            ],
            "seasons": [
                "mavuno",
                "baridi kali",
                "kuchanua",
                "masika",
                "mzunguko wa jua",
                "kijani kibichi",
                "kuyeyuka",
                "rangi ya dhahabu",
                "baridi",
                "upya"
            ]
        }

_THEME_WORDS_FR = {
            "nature": [
                "forêt",
                "rivière",
                "montagne",
                "océan",
                "brise",
                "prairie",
                "soleil",
                "tonnerre",
                "fleur",
                "pierre",
                "horizon",
                "rosée"
            ],
            "love": [
                "cœur",
                "chaleur",
                "étreinte",
                "désir",
                "douceur",
                "toujours",
                "tendre",
                "dévotion",
                "proximité",
                "doucement",
                "chérir",
                "éclat"
            ],
            "time": [
                "instant",
                "souvenir",
                "demain",
                "hier",
                "horloge",
                "fugace",
                "patience",
                "saison",
                "aube",
                "crépuscule",
                "heure"
            ],
            "space": [
                "galaxie",
                "lumière d'étoile",
                "orbite",
                "comète",
                "nébuleuse",
                "cosmos",
                "gravité",
                "voyage",
                "infini",
                "poussière d'étoile",
                "météore"
            ],
            "general": [
                "merveille",
                "courage",
                "silence",
                "voyage",
                "ombre",
                "écho",
                "étincelle",
                "horizon",
                "errer",
                "calme",
                "lumineux"
            ],
            "friendship": [
                "rire",
                "loyauté",
                "proche",
                "confiance",
                "compagnie",
                "fidèle",
                "chaleur",
                "appartenance",
                "partagé",
                "ensemble"
            ],
            "seasons": [
                "récolte",
                "givre",
                "floraison",
                "mousson",
                "solstice",
                "toujours vert",
                "dégel",
                "ambre",
                "froid",
                "renouveau"
            ]
        }

_RHYME_BANK_SW = {
            "moyoni": [
                "ndani",
                "polepole",
                "kimya"
            ],
            "safari": [
                "mori",
                "kesho",
                "dari"
            ],
            "milele": [
                "hale",
                "sele",
                "amani ile"
            ],
            "upendo": [
                "mwendo",
                "ndondondo",
                "wimbo"
            ],
            "furaha": [
                "baraka",
                "faraja",
                "raha"
            ],
            "matumaini": [
                "mabaya kwaheri",
                "usoni",
                "moyoni"
            ],
            "amani": [
                "nyumbani",
                "mioyoni",
                "milimani"
            ],
            "nuru": [
                "dunia nzuru",
                "shauku",
                "sauti safi"
            ],
            "njia": [
                "ndia",
                "mbia",
                "ardhia"
            ],
            "wimbo": [
                "ombo",
                "sambo",
                "kombo"
            ]
        }

_RHYME_BANK_FR = {
            "lumière": [
                "rivière",
                "prière",
                "fougère"
            ],
            "nuit": [
                "ennui",
                "fruit",
                "pluie"
            ],
            "jour": [
                "amour",
                "toujours",
                "détour"
            ],
            "mer": [
                "hiver",
                "clair",
                "air"
            ],
            "ciel": [
                "réel",
                "essentiel",
                "éternel"
            ],
            "cœur": [
                "bonheur",
                "chaleur",
                "douceur"
            ],
            "temps": [
                "printemps",
                "vent",
                "moment"
            ],
            "rêve": [
                "sève",
                "grève",
                "achève"
            ],
            "route": [
                "doute",
                "écoute",
                "voûte"
            ],
            "âme": [
                "flamme",
                "femme",
                "trame"
            ]
        }

_ACROSTIC_SW = {
            "A": [
                "subuhi huleta matumaini mapya"
            ],
            "B": [
                "ahari hunong'ona siri zake"
            ],
            "C": [
                "hemchemi hutiririka bila kikomo"
            ],
            "D": [
                "unia hugeuka polepole kila siku"
            ],
            "E": [
                "limu hufungua milango mingi"
            ],
            "F": [
                "uraha hujificha kwenye vitu vidogo"
            ],
            "G": [
                "iza hupita, mwanga hufuata"
            ],
            "H": [
                "isia huja na kuondoka kama mawimbi"
            ],
            "I": [
                "mani husimama hata dhoruba ikivuma"
            ],
            "J": [
                "ua huchomoza tena kesho"
            ],
            "K": [
                "umbukumbu hubaki hata baada ya miaka"
            ],
            "L": [
                "engo huja kwa uvumilivu"
            ],
            "M": [
                "vua huleta uzima kwenye ardhi kavu"
            ],
            "N": [
                "yota huangaza hata gizani"
            ],
            "O": [
                "mbi la kweli halipotei"
            ],
            "P": [
                "endo halichoki kungoja"
            ],
            "Q": [
                " ni herufi nadra, lakini bado ina nafasi yake"
            ],
            "R": [
                "afiki wa kweli hubaki karibu"
            ],
            "S": [
                "afari ndefu huanza na hatua moja"
            ],
            "T": [
                "umaini huishi hata gizani"
            ],
            "U": [
                "pendo hauna mipaka"
            ],
            "V": [
                "umbi la jana huachwa nyuma"
            ],
            "W": [
                "imbo wa moyo huwa wa kweli daima"
            ],
            "X": [
                " ni ishara ya kile kisichojulikana bado"
            ],
            "Y": [
                "aliyopita hufundisha yajayo"
            ],
            "Z": [
                "awadi kubwa mara nyingi huwa ndogo"
            ]
        }

_ACROSTIC_FR = {
            "A": [
                "ube nouvelle apporte l'espoir"
            ],
            "B": [
                "rise légère chante doucement"
            ],
            "C": [
                "haque instant compte à sa façon"
            ],
            "D": [
                "ouceur du soir apaise l'âme"
            ],
            "E": [
                "toile filante porte un vœu"
            ],
            "F": [
                "eu qui danse réchauffe le cœur"
            ],
            "G": [
                "râce silencieuse guide nos pas"
            ],
            "H": [
                "orizon lointain appelle les rêveurs"
            ],
            "I": [
                "nstant présent mérite d'être vécu"
            ],
            "J": [
                "ardin secret garde ses couleurs"
            ],
            "K": [
                "aléidoscope de couleurs danse au vent"
            ],
            "L": [
                "umière douce traverse la fenêtre"
            ],
            "M": [
                "arée montante efface les traces"
            ],
            "N": [
                "uage passager cache le soleil"
            ],
            "O": [
                "mbre légère suit chaque pas"
            ],
            "P": [
                "luie fine murmure sur le toit"
            ],
            "Q": [
                "uiétude du soir enveloppe la ville"
            ],
            "R": [
                "êve oublié revient parfois"
            ],
            "S": [
                "ilence profond parle plus fort que les mots"
            ],
            "T": [
                "emps qui passe laisse des traces douces"
            ],
            "U": [
                "nivers infini garde ses mystères"
            ],
            "V": [
                "ent léger chuchote une chanson"
            ],
            "W": [
                "agon du souvenir avance lentement"
            ],
            "X": [
                "ylophone lointain résonne doucement"
            ],
            "Y": [
                "eux fermés, le cœur voit mieux"
            ],
            "Z": [
                "este de vie parfume chaque jour"
            ]
        }

_HAIKU_SW = {
            "1": [
                "theluji inaanguka polepole",
                "mto unatiririka kimya",
                "majani yanapeperushwa na upepo",
                "asubuhi inagusa vilima",
                "nyota zinameremeta juu",
                "mvua inagonga kioo",
                "mlango wa zamani unalia",
                "baridi inafunika shamba",
                "moshi unapaa kutoka motoni",
                "bwawa liko kimya kabisa"
            ],
            "2": [
                "na ukimya unatawala kila kitu",
                "wakati bonde linashikilia pumzi",
                "mwanga mmoja gizani",
                "hakuna kinachosonga isipokuwa upepo",
                "msimu unabadilika tena",
                "na ukimya unajibu kwa upole",
                "vivuli vinajinyoosha njiani",
                "korongo linasubiri kwenye matete",
                "asubuhi inasubiri mlangoni",
                "dunia inapumua na kutulia"
            ],
            "3": [
                "mwezi unapanda angani",
                "maua yanagusa ardhi",
                "upepo unapita matete",
                "bustani sasa inalala",
                "mawimbi yanafika ufukweni",
                "nyota zinang'aa kimya",
                "jua linatua polepole",
                "ndege wanaruka mbali"
            ]
        }

_HAIKU_FR = {
            "1": [
                "la neige tombe doucement",
                "la rivière coule lentement",
                "les feuilles dansent au vent",
                "le matin touche les collines",
                "les étoiles scintillent",
                "la pluie frappe la vitre",
                "la vieille porte grince",
                "le givre couvre le champ",
                "la fumée monte du feu",
                "l'étang reste immobile"
            ],
            "2": [
                "et le silence s'installe",
                "pendant que la vallée retient son souffle",
                "une seule lumière dans le noir",
                "et rien ne bouge sauf le vent",
                "la saison tourne encore une fois",
                "et le silence répond doucement",
                "les ombres s'étirent le long du chemin",
                "un héron attend dans les roseaux",
                "le matin attend à la porte",
                "le monde expire et se calme"
            ],
            "3": [
                "la lune monte dans le ciel",
                "les pétales touchent le sol",
                "le vent traverse les roseaux",
                "le jardin dort maintenant",
                "les vagues atteignent la rive",
                "les étoiles brillent en silence",
                "le soleil se couche doucement",
                "les oiseaux s'envolent au loin"
            ]
        }



class PoemWriter:
    """
    Generates poems using purely rule-based templates:
      - Acrostic poems (first letters spell a word, e.g. the user's name)
      - Haiku-style poems (5-7-5 syllable rule for English, approximated
        with a simple rule-based syllable counter - no ML, no dictionary
        lookups online; Swahili/French use a fixed, hand-checked line bank
        instead, since the English vowel-counting heuristic below doesn't
        model those languages' syllable/liaison rules)
      - Rhyming couplets (built from a small hand-written rhyme dictionary
        per language)

    None of this involves training or learning; it is template filling
    plus deterministic rules (syllable heuristics, rhyme lookups).
    """

    # Word banks, organized by theme, one per language (en/sw/fr) so the
    # acrostic and couplet generators can respond in whichever language
    # LanguageDetector identified, same idea as the Section 8 response
    # banks. Swahili and French word choices are separate translations,
    # not literal word-for-word substitutions, so the resulting lines
    # still read naturally in each language.
    _THEME_WORDS_EN = {
        "nature": ["forest", "river", "mountain", "ocean", "breeze", "meadow",
                   "sunlight", "thunder", "blossom", "stone", "horizon", "dew"],
        "love": ["heart", "warmth", "embrace", "longing", "gentle", "forever",
                 "tender", "devotion", "closeness", "softly", "cherish", "glow"],
        "time": ["moment", "memory", "tomorrow", "yesterday", "clockwork",
                 "fleeting", "patience", "season", "dawn", "twilight", "hour"],
        "space": ["galaxy", "starlight", "orbit", "comet", "nebula", "cosmos",
                  "gravity", "voyage", "infinite", "stardust", "meteor"],
        "general": ["wonder", "courage", "silence", "journey", "shadow",
                    "echo", "spark", "horizon", "wander", "quiet", "bright"],
        "friendship": ["laughter", "loyalty", "kindred", "trust", "company",
                       "steadfast", "warmth", "belonging", "shared", "together"],
        "seasons": ["harvest", "frost", "bloom", "monsoon", "solstice",
                    "evergreen", "thaw", "amber", "chill", "renewal"],
    }

    THEME_WORDS = {"en": _THEME_WORDS_EN, "sw": _THEME_WORDS_SW, "fr": _THEME_WORDS_FR}

    # A small hand-written rhyme dictionary per language: word -> list of
    # words that rhyme with it. Deliberately small and explicit (rigid,
    # not learned). The Swahili and French banks use anchor words natural
    # to those languages rather than translating the English anchors.
    _RHYME_BANK_EN = {
        "light": ["night", "bright", "sight", "flight", "delight"],
        "night": ["light", "bright", "sight", "flight", "delight"],
        "day": ["away", "play", "stay", "ray", "gray"],
        "sea": ["free", "be", "tree", "key", "glee"],
        "heart": ["start", "part", "art", "apart"],
        "sky": ["high", "fly", "by", "why"],
        "rain": ["again", "pain", "remain", "plain", "chain"],
        "dream": ["stream", "gleam", "beam", "seem", "team"],
        "star": ["far", "are", "scar", "afar"],
        "moon": ["soon", "tune", "june", "balloon"],
        "shore": ["more", "before", "door", "explore"],
        "wind": ["pinned", "thinned", "skinned"],
        "fire": ["desire", "higher", "inspire", "tire"],
        "snow": ["glow", "grow", "slow", "below"],
        "friend": ["mend", "bend", "send", "defend"],
        "road": ["load", "bestowed", "flowed", "glowed"],
        "hope": ["scope", "slope", "rope", "cope"],
        "gold": ["bold", "told", "cold", "unfold"],
        "smile": ["mile", "while", "style", "worthwhile"],
    }

    RHYME_BANK = {"en": _RHYME_BANK_EN, "sw": _RHYME_BANK_SW, "fr": _RHYME_BANK_FR}

    VOWELS = "aeiouy"

    # ---- syllable counting -------------------------------------------------

    def count_syllables(self, word: str) -> int:
        """
        A simple, rigid heuristic syllable counter (no dictionary lookup,
        no ML): count vowel groups, with a small correction for silent
        trailing 'e'. This is the same kind of heuristic widely used in
        rule-based text tools; it isn't perfectly accurate but is fast,
        deterministic, and fully offline. Tuned for English only - see
        the haiku() docstring for how Swahili/French sidestep this.
        """
        word = word.lower().strip(string.punctuation)
        if not word:
            return 0

        count = 0
        prev_was_vowel = False
        for ch in word:
            is_vowel = ch in self.VOWELS
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel

        if word.endswith("e") and count > 1 and not word.endswith("le"):
            count -= 1

        return max(count, 1)

    def count_line_syllables(self, line: str) -> int:
        words = re.findall(r"[a-zA-Z']+", line)
        return sum(self.count_syllables(w) for w in words)

    # ---- acrostic -----------------------------------------------------------

    def acrostic(self, word: str, lang: str = "en") -> str:
        """Build an acrostic poem where each line starts with successive
        letters of `word`, using theme-relevant phrase fragments in
        whichever of the three languages was requested."""
        word = re.sub(r"[^a-zA-Z]", "", word).upper()
        if not word:
            word = "HELLO"

        fragments_by_letter = self._build_letter_fragments(lang)
        fallback = {
            "en": "is a quiet wonder all its own",
            "sw": "ni ajabu ya kimya ya pekee yake",
            "fr": "est une merveille silencieuse à part entière",
        }.get(lang, "is a quiet wonder all its own")
        lines = []
        for letter in word:
            options = fragments_by_letter.get(letter)
            if options:
                fragment = random.choice(options)
            else:
                fragment = fallback
            lines.append(f"{letter}{fragment}")
        return "\n".join(lines)

    @staticmethod
    def _build_letter_fragments(lang: str = "en"):
        """A hand-written bank of line-completions keyed by starting letter,
        designed so the acrostic reads naturally regardless of the input
        word, in whichever language was requested."""
        en_fragments = {
            "A": ["lways reaching for the light", "wakens something deep inside", "ll at once, the quiet shifts"],
            "B": ["right as morning's first hour", "eyond the hills, a calm unfolds", "old enough to chase the dawn"],
            "C": ["arried gently on the breeze", "alm settles over everything", "limbing slowly toward the sun"],
            "D": ["rifting like a feather down", "ay breaks soft across the field", "eep within, a quiet spark"],
            "E": ["very moment holds a story", "choes linger in the dark", "ndless as the open sky"],
            "F": ["orever changing, never still", "ar beyond what eyes can see", "alling gently into place"],
            "G": ["entle as the evening tide", "rowing stronger every day", "lowing softly, warm and slow"],
            "H": ["olding fast to what remains", "ere, the silence speaks the loudest", "opeful even in the rain"],
            "I": ["nside, a thousand colors bloom", "magine all that's still to come", "n the stillness, something grows"],
            "J": ["ourneys further than they seem", "oy arrives without a warning", "ust beyond the next horizon"],
            "K": ["eeping every promise made", "ind words travel further still", "nown only to the patient heart"],
            "L": ["ight finds its way through every crack", "ingers longer than expected", "ooking forward, not behind"],
            "M": ["oves like water, finds its way", "akes a home in unlikely places", "orning always finds a way"],
            "N": ["ever quite the way it seemed", "othing stays exactly still", "ear enough to almost touch"],
            "O": ["pens slowly, like a door", "nce in every quiet while", "ut beyond the furthest edge"],
            "P": ["atience pays in ways unseen", "asses gently, hand to hand", "ainted soft in fading light"],
            "Q": ["uietly the answer comes", "uestions linger, unafraid", "uick as a passing thought"],
            "R": ["ises even after falling", "emembers everything it's lost", "eaches farther than it knows"],
            "S": ["tarts again with every breath", "oftly, surely, finds its place", "hines through every kind of weather"],
            "T": ["ravels farther than it planned", "ime forgives what time has broken", "ouches lightly, leaves a mark"],
            "U": ["nfolds in its own good time", "nderneath it all, still steady", "p ahead, the path grows clear"],
            "V": ["entures out beyond the known", "oices carry on the wind"],
            "W": ["anders without losing heart", "aits patiently for morning", "onders what the day will bring"],
            "X": [" marks a place still unexplored"],
            "Y": ["ields to nothing but the dawn", "earns for something just ahead"],
            "Z": ["ig-zags softly toward the light", "ero in on what remains"],
        }
        if lang == "sw":
            return _ACROSTIC_SW
        if lang == "fr":
            return _ACROSTIC_FR
        return en_fragments

    # ---- haiku ---------------------------------------------------------------

    HAIKU_LINE_BANK = {
        5: [
            "snow falls on the roof", "the river runs slow", "leaves drift on the wind",
            "morning finds the hills", "stars blink overhead", "rain taps on the glass",
            "the old door creaks shut", "frost covers the field", "smoke curls from the fire",
            "the pond sits so still", "petals touch the ground", "the moon climbs the sky",
            "wind moves through the reeds", "the garden sleeps now", "waves reach for the shore",
        ],
        7: [
            "and quiet settles in close", "while the valley holds its breath",
            "a single light in the dark", "and nothing moves but the wind",
            "the season turns once again", "and silence answers softly",
            "while shadows stretch down the lane", "a heron waits in the reeds",
            "and morning waits at the door", "the world exhales and grows still",
            "while distant thunder replies", "and the fields turn gold and gray",
        ],
    }

    # Swahili/French haiku-style line pools, keyed by line position
    # (1/2/3) rather than syllable count - see the haiku() docstring for
    # why these bypass the English syllable heuristic entirely.
    HAIKU_LINE_BANK_SW = _HAIKU_SW
    HAIKU_LINE_BANK_FR = _HAIKU_FR

    def haiku(self, topic: str = None, lang: str = "en") -> str:
        """
        Build a 3-line haiku-style poem. For English this follows the
        classic 5-7-5 syllable rule, with lines assembled from a
        hand-written bank and verified against the rule-based syllable
        counter, plus an optional topic word woven into the first line
        when it fits cleanly. For Swahili and French, syllable counting
        with an English-tuned vowel heuristic isn't linguistically valid
        (different vowel/liaison rules), so those two languages instead
        draw from their own fixed, hand-checked 3-line pools - still
        template filling, just without the syllable-count verification
        step that only makes sense for English.
        """
        if lang == "sw":
            pool = self.HAIKU_LINE_BANK_SW
            return f"{random.choice(pool['1'])}\n{random.choice(pool['2'])}\n{random.choice(pool['3'])}"
        if lang == "fr":
            pool = self.HAIKU_LINE_BANK_FR
            return f"{random.choice(pool['1'])}\n{random.choice(pool['2'])}\n{random.choice(pool['3'])}"

        line1_options = list(self.HAIKU_LINE_BANK[5])
        line2_options = list(self.HAIKU_LINE_BANK[7])
        line3_options = list(self.HAIKU_LINE_BANK[5])

        if topic:
            topic_clean = re.sub(r"[^a-zA-Z\s]", "", topic).strip().lower()
            if topic_clean:
                syl = self.count_syllables(topic_clean.split()[0])
                if syl <= 3:
                    candidate = f"{topic_clean} in the light"
                    if self.count_line_syllables(candidate) == 5:
                        line1_options.insert(0, candidate)

        line1 = random.choice(line1_options)
        line2 = random.choice(line2_options)
        line3 = random.choice(line3_options)

        # Verify syllable counts; if our heuristic disagrees (rare, given
        # the bank was hand-checked), fall back to safe defaults.
        if self.count_line_syllables(line1) != 5:
            line1 = "snow falls on the roof"
        if self.count_line_syllables(line2) != 7:
            line2 = "and quiet settles in close"
        if self.count_line_syllables(line3) != 5:
            line3 = "stars blink overhead"

        # Avoid the (visually awkward) case where line 1 and line 3 end up
        # being the exact same line - this can happen either from the
        # random pick above (both pools share the same 5-syllable bank)
        # or from both lines independently hitting the same syllable
        # fallback string, so this check must run AFTER the fallback logic
        # above, not before it.
        if line3 == line1:
            alternatives = [l for l in self.HAIKU_LINE_BANK[5] if l != line1]
            if alternatives:
                line3 = random.choice(alternatives)

        return f"{line1}\n{line2}\n{line3}"

    # ---- rhyming couplets -----------------------------------------------------

    @staticmethod
    def _article_for(word: str, lang: str = "en") -> str:
        """Return 'an'/'a' (English), or the appropriate short lead-in for
        Swahili/French. Swahili nouns don't take an indefinite article at
        all, so this returns an empty string for "sw". French distinguishes
        "un"/"une" by grammatical gender, which a first-letter heuristic
        can't determine correctly, so a neutral "un/une" placeholder is
        avoided in favor of just using "un" (the far more common case
        across this word bank's simple nouns) - a small, acknowledged
        simplification, not a full grammatical-gender model."""
        if lang == "sw":
            return ""
        if lang == "fr":
            return "un"
        return "an" if word and word[0].lower() in "aeiou" else "a"

    def rhyming_couplets(self, theme: str = "general", num_couplets: int = 2, lang: str = "en") -> str:
        """Build a short rhyming poem (AABB pattern) from the rhyme bank
        and theme word list for whichever language was requested."""
        theme_words_all = self.THEME_WORDS.get(lang, self.THEME_WORDS["en"])
        theme = theme.lower().strip()
        if theme not in theme_words_all:
            theme = "general"
        words = theme_words_all[theme]

        rhyme_bank = self.RHYME_BANK.get(lang, self.RHYME_BANK["en"])
        rhyme_anchors = list(rhyme_bank.keys())
        random.shuffle(rhyme_anchors)

        templates = {
            "en": lambda w1, article1, anchor, article2, w2, partner:
                (f"The {w1} calls where {article1} {anchor} may be,",
                 f"{article2} {w2} answers, wild and free, like {partner} drifting endlessly."),
            "sw": lambda w1, article1, anchor, article2, w2, partner:
                (f"{w1.capitalize()} huita mahali {anchor} inapoweza kuwa,",
                 f"{w2.capitalize()} hujibu, huru na bila mipaka, kama {partner} ikielea milele."),
            "fr": lambda w1, article1, anchor, article2, w2, partner:
                (f"Le {w1} appelle là où {article1} {anchor} pourrait être,",
                 f"{article2.capitalize()} {w2} répond, libre et sans limites, comme {partner} qui dérive à jamais."),
        }
        template = templates.get(lang, templates["en"])

        fallback = {
            "en": ["The world keeps turning, soft and slow,", "a quiet rhythm only hearts may know."],
            "sw": ["Dunia inaendelea kuzunguka, kwa upole na polepole,", "mdundo wa kimya ambao ni mioyo tu inayoujua."],
            "fr": ["Le monde continue de tourner, doux et lent,", "un rythme discret que seuls les cœurs comprennent."],
        }.get(lang, ["The world keeps turning, soft and slow,", "a quiet rhythm only hearts may know."])

        lines = []
        for i in range(num_couplets):
            if i >= len(rhyme_anchors):
                break
            anchor = rhyme_anchors[i]
            partner = random.choice(rhyme_bank[anchor])
            w1 = random.choice(words)
            w2 = random.choice(words)
            article1 = self._article_for(anchor, lang)
            article2 = self._article_for(w2, lang)
            line_a, line_b = template(w1, article1, anchor, article2, w2, partner)
            lines.append(line_a)
            lines.append(line_b)
        if not lines:
            lines = fallback
        return "\n".join(lines)

# ==============================================================================
