# Ciderhouse - Experiments in SRE and Home-Brewing

I'm Jezza, and I'm descended from squirrels. I get bored easily, I enjoy tinkering, and I love new projects that give me
and opportunty to learn new things.

Many moons ago, I was on a trip in Dorset and we visited a country pub near Swanage, which I believe was the [Square and
Compass](https://www.squareandcompasspub.co.uk/). I remember being very taken by the cider, which was apparently brewed
locally and tasted totally different to
the commercial ciders I was familiar with at that point.

Many years later, I need a project, and the internal squirrel brain settled on the idea of doing some home fermentation.
I've fermented beer before, which was drinkable but nothing special. Given that I live in Kent and am surrounded by
apple orchards, it seemed a good idea to investigate cider-making.

From experience, I knew I'd need some things, and I'd need to learn some other things. But one thing I definitely wanted
to do was have some way to observe and track the fermentation process from the comfort of anywhere but the
spider-infested horror that doubles as my garage.

I also needed some way to protect my fermentation set-up from accidental kicks or other hazards, like having a spade
fall on it.

My daytime job is SRE, so I decided to SRE the ~~censored~~ out of this.

#### The Cider Fermentation Lifecycle

There are several stages

1. Preparation
2. Primary fermentation
3. Bottling and secondary fermentation
4. Clarifying
5. Consumption

Of these steps, 1. and 2. are probably the most critical, as they present the biggest risk of contamination or
catastrophe.

I decided that as romantic as the idea of collecting and crushing apples might sound, the reality would likely be hot
and monotonous. Instead, I will
be purchasing 5l of organic apple juice from one of Kent's many orchards and using that as my stock. There is a list of
things that are required for a basic
home-brewing setup, most of which are detailed below.

###### A non-exhaustive list of physical infrastructure

| Item                                                            | Cost       | Description                                                                                                                                                                                                                                                                                                                                                                                                      |
|-----------------------------------------------------------------|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Campden tablets](https://en.wikipedia.org/wiki/Campden_tablet) | £5         | A sulphur-based compound that is used to sterilize fermentation mix before the actual fermentation is begun 24 - 48h later                                                                                                                                                                                                                                                                                       |
| Malic Acid                                                      | £3         | Malic acid is an organic compound that gives fruit its sour / acidic taste.  If the apple juice used to brew the cider is short on "tart" apples, then adding additional malic acid can correct this before fermentation takes place, giving a crisper cider - apparently.  Basically, if your apple juice is too low in pH, add this to bring it back to the desired range                                      |
| Precipitated chalk                                              | £3         | A base, added to your juice before fermentation if the pH is too low. you add chalk to bring it back to the desired range.                                                                                                                                                                                                                                                                                       |
| pH testing strips                                               | £3         | The tongue is not a good indicator of acidity.  Universal Indicator is.                                                                                                                                                                                                                                                                                                                                          |
| No-rinse steriliser - Sodium Percarbonate                       | £10        | A chemical agent that will sterilize and sanitize brewing equipment without leaving a residue that can interfere with fermentation.  Used to sterilize and sanitize equipment before use                                                                                                                                                                                                                         |
| Fermentation vessel                                             | £5 - £20   | The fermentation vessel needs to be a sterile, food-safe container in which the primary fermentation of apple juice can take place.<br/>Typically this would be glass - a vessel called a [Demijohn](https://dictionary.cambridge.org/images/thumb/demijo_noun_004_1050.jpg?version=6.0.53) is often used for home wine brewing.  However, more modern plastic vessels exist which are a lot safer to work with. |
| Airlock                                                         | £2         | An airlock is a shaped piece of glass or other materiel that can prevent oxygen from entering the fermentation vessel while permitting carbon dioxide to escape, thus preventing a failure due to overpressure of the fermentation vessel.                                                                                                                                                                       |
| Thermometer                                                     | £3 upwards | A thermometer is necessary to ensure the fermentation reaction is not too hot (runs too fast, can create undesired compounds, kills the yeast) or too cold (pauses the reaction, potentially kills the yeast)                                                                                                                                                                                                    |
| Hydrometer                                                      | £6 and up  | A hydrometer is a device that is used to measure the specific gravity of a fluid.  In brewing and fermenting it is used to determine the density, and from a gradiated scale it is possible to read off the change in sugar volume and thus the proportion of alcohol in the mixture.                                                                                                                            |
| Yeast                                                           | £1.50      | It is entirely possible to ferment based on natural yeasts present in the fruit, but this can be an exciting process and I'm not brave enough.  Using packaged single-variety yeast should give a more controlled reaction while minimising risk.                                                                                                                                                                |

There is a secondary equipment requirement for bottling the results of the primary fermentation. I will talk through
bottling [here](./bottling.md)

This is great, and with all of this equipment I can probably make cider. But it will be very manual - so let's automate
one or two things.

[Part 2 >>](control-system.md)

